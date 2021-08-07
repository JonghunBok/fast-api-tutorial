from typing import List, Optional

from fastapi import Depends, FastAPI, Header, HTTPException


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

async def verify_token(x_token: str = Header(...)):
    if x_token != "fake_token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

app = FastAPI(dependencies=[Depends(verify_token)])

@app.get("/items/", dependencies=[Depends(verify_token)])
async def read_items(commons: CommonQueryParams = Depends()):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


