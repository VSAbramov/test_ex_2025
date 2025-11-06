from pydantic import BaseModel, Field


class AddItemToOrderInputSchema(BaseModel):
    order_id: int = Field(ge=0)
    item_id: int = Field(ge=0)
    quantity: int = Field(gt=0)


class AddItemToOrderOutputSchema(AddItemToOrderInputSchema):
    price: int = Field(ge=0)


class HTTPError(BaseModel):
    detail: str
