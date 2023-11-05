from pydantic import BaseModel
from typing import List

class Song(BaseModel):
    title: str
    keywords: List[str]