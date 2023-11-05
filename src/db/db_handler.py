from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["music_db"]
collection = db["songs"]

def add_song(song_data):
    result = collection.insert_one(song_data)
    return str(result.inserted_id)

# 특정 키워드로 노래를 검색하는 함수
def search_song_by_keyword(keyword):
    songs = collection.find({"keywords": keyword})
    song_list = [song["title"] for song in songs]
    return song_list
