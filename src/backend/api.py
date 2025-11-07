from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from backend.crud import InvalidArgs, add_item
from backend.database import get_db_session
from backend.schemas import (
    AddItemToOrderInputSchema,
    AddItemToOrderOutputSchema,
    HTTPError,
)

router = APIRouter()


@router.post(
    "/add-item",
    response_model=AddItemToOrderOutputSchema,
    responses={
        404: {"model": HTTPError, "description": "Validation error"},
        422: {"model": HTTPError, "description": "Arguments are in conflict"},
    },
)
def add_item_to_order(
    input: AddItemToOrderInputSchema,
    db: Session = Depends(get_db_session),
):
    try:
        order_item = add_item(
            db, input.order_id, input.item_id, input.quantity
        )
    except InvalidArgs as e:
        raise HTTPException(status_code=422, detail=str(e))
    return AddItemToOrderOutputSchema(
        order_id=order_item.order_id,
        item_id=order_item.item_id,
        quantity=order_item.quantity,
        unit_price=order_item.unit_price,
    )
