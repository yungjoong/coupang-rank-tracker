from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

class ProductSearch(BaseModel):
    keyword: str
    url: str

class KeywordBase(BaseModel):
    keyword: str

class KeywordCreate(KeywordBase):
    pass

class Keyword(KeywordBase):
    id: int
    product_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductBase(BaseModel):
    url: str
    name: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    keywords: List[Keyword] = []

    model_config = ConfigDict(from_attributes=True)

class ProductWithKeywords(Product):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)