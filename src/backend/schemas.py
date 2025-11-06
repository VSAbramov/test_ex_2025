from pydantic import BaseModel, ConfigDict, Field


class AddItemToOrderInputSchema(BaseModel):
    order_id: int = Field(ge=0)
    item_id: int = Field(ge=0)
    quantity: int = Field(gt=0)


class AddItemToOrderOutputSchema(AddItemToOrderInputSchema):
    model_config = ConfigDict(from_attributes=True)
    unit_price: float = Field(ge=0)


class HTTPError(BaseModel):
    detail: str
