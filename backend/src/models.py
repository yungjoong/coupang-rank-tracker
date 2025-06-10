from pydantic import BaseModel

class ProductSearch(BaseModel):
    keyword: str
    url: str