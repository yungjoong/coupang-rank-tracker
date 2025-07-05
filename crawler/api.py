from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .coupang_rank_crawler import get_coupang_product_rank
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RankRequest(BaseModel):
    search_keyword: str
    product_url: str
    max_pages: int = 5

class RankResponse(BaseModel):
    rank: Optional[int]
    page: Optional[int]
    message: Optional[str] = None
    links: List[str] = []
    screenshots: List[str] = []

@app.post("/rank", response_model=RankResponse)
def get_rank(req: RankRequest):
    result = get_coupang_product_rank(req.search_keyword, req.product_url, req.max_pages)
    return RankResponse(
        rank=result.get("rank"),
        page=result.get("page"),
        message=result.get("message", "상품이 검색 결과에 없습니다."),
        links=result.get("links", []),
        screenshots=result.get("screenshots", [])
    )