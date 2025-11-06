from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models import Item, Order, OrderItem


class InvalidArgs(Exception):
    pass


def add_item(
    db: Session, order_id: int, item_id: int, quantity: int
) -> OrderItem:
    item = db.get(Item, item_id)
    if item is None:
        raise InvalidArgs(f"Item with id: {item_id} doesn't exist")
    if item.quantity < quantity:
        raise InvalidArgs(f"Only {item.quantity} of {item.name} left")
    order = db.get(Order, order_id)
    if order is None:
        raise InvalidArgs(f"Order with id: {order_id} doesn't exist")

    order_item_query: OrderItem = select(OrderItem).where(
        (OrderItem.order_id == order_id) & (OrderItem.item_id == item_id)
    )
    order_items = db.scalars(order_item_query).all()
    if len(order_items) == 1:
        order_item = order_items[0]
    else:
        order_item = OrderItem(
            order_id=order_id,
            item_id=item_id,
            quantity=quantity,
            unit_price=item.price,
        )
        db.add(order_item)

    order_item.quantity += quantity
    item.quantity -= quantity
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    return order_item
