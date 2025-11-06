import logging

import conftest
import pytest
from lib import get_head
from sqlalchemy import select

from backend.crud import add_item
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


def test_add_item_works(session, order_f):
    # call function
    item_id = 1
    new_order_item = add_item(session, order_f.id, item_id, 1)

    # assert record inside db
    order_item_query: OrderItem = select(OrderItem).where(
        (OrderItem.order_id == order_f.id) & (OrderItem.item_id == item_id)
    )
    db_order_item = session.scalars(order_item_query).first()
    assert db_order_item == new_order_item
