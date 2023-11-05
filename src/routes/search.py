from fastapi import APIRouter
from src.db.db_handler import search_song_by_keyword

router = APIRouter()

@router.get("/search_song/")
async def search_song(keyword: str):
    song_list = search_song_by_keyword(keyword)
    if song_list:
        return {"songs": song_list}
    else:
        return {"message": "No songs found for the keyword."}
