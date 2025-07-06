from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Tuple
from .recommender import OTTRecommender

app = FastAPI()
recommender = OTTRecommender()

class RecommendationRequest(BaseModel):
    title: str
    platform_filter: Optional[List[str]] = None
    year_range: Optional[Tuple[int, int]] = None
    duration_range: Optional[Tuple[int, int]] = None
    top_n: int = 10

@app.post("/recommend")
async def recommend_movies(request: RecommendationRequest):
    results = recommender.recommend(
        title=request.title,
        platform_filter=request.platform_filter,
        year_range=request.year_range,
        duration_range=request.duration_range,
        top_n=request.top_n
    )
    return {"results": results}

@app.get("/")
async def root():
    return {"message": "OTT Recommender API is running"}