from fastapi import FastAPI, Body, Path, Cookie, Header
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", example="This is a field example", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice form",
                "price": 45.3,
                "tax": 3.2,
            }
        }

@app.get("/items/")
async def read_items(ads_id: Optional[str] = Cookie(None), x_token: Optional[List[str]] = Header(None)):
    return {"ads_id": ads_id, "X-Token values": x_token}


@app.get("/itmes/{item_id}")
async def read_items(
    q: str,
    item_id: int = Path(..., title="The ID of the item to get"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

@app.put("/itmes/{itme_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        ...,
        example={
            "name": "Foo2",
            "description": "A very nice form",
            "price": 45.3,
            "tax": 3.2,
        },
    )
):
    results = {"item_id": item_id, "item": item}
    return results
