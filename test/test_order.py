import logging

import conftest
import pytest
from lib import get_head
from sqlalchemy import func, select

from backend.crud import InvalidArgs, add_item
from backend.models import Category, Item, Order, OrderItem


@pytest.fixture(scope="function")
def order_f(session) -> Order:
    order = Order(client_id=0)
    session.add(order)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(order)
    return order


def test_add_item_create_works(session, order_f):
    # call function
    item_id = 1
    quantity = 1
    item = session.get(Item, item_id)
    quantity_left_before = item.quantity
    new_order_item = add_item(session, order_f.id, item_id, quantity)

    # assert record inside db
    order_item_query: OrderItem = select(OrderItem).where(
        (OrderItem.order_id == order_f.id) & (OrderItem.item_id == item_id)
    )

    db_order_item = session.scalars(order_item_query).first()
    assert db_order_item == new_order_item
    item = session.get(Item, item_id)
    quantity_left_after = item.quantity
    assert quantity_left_before - quantity_left_after == quantity


def test_add_item_increase_works(session, order_f):
    item_id = 1
    quantity = 1
    order_item = add_item(session, order_f.id, item_id, quantity)
    quant_before = order_item.quantity
    order_item = add_item(session, order_f.id, item_id, quantity)
    assert order_item.quantity - quant_before == quantity


def test_add_item_invalid_args_fails(session, order_f):
    item_id = 1

    # wrong order id
    invalid_order_id = session.query(func.max(Order.id)).scalar() + 1
    with pytest.raises(InvalidArgs):
        add_item(session, invalid_order_id, item_id, 1)

    # wrong item id
    invalid_item_id = session.query(func.max(Item.id)).scalar() + 1
    with pytest.raises(InvalidArgs):
        add_item(session, order_f.id, invalid_item_id, 1)

    # wrong quantity
    item = session.get(Item, item_id)
    invalid_quantity = item.quantity + 1
    with pytest.raises(InvalidArgs):
        add_item(session, order_f.id, item_id, invalid_quantity)
    with pytest.raises(InvalidArgs):
        add_item(session, order_f.id, item_id, -1)
