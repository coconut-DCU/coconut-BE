import requests
import base64

from ..settings.spotify_config import *
from .image_to_song import get_recommend_songs

def get_access_token(client_id, client_secret):
    encoded = base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('ascii')
    headers = {"Authorization": f"Basic {encoded}"}
    payload = {"grant_type": "client_credentials"}
    response = requests.post("https://accounts.spotify.com/api/token", data=payload, headers=headers)
    return response.json()['access_token']

def search_spotify(query, query_type, access_token):
    params = {"q": query, "type": query_type, "limit": "1"}
    response = requests.get("https://api.spotify.com/v1/search", params=params, headers={"Authorization": f"Bearer {access_token}"})
    data = response.json().get(f'{query_type}s', {}).get('items', [])
    return data[0]


access_token = get_access_token(CLIENT_ID, CLIENT_KEY)

album_info = {
    "Permission to Dance": "BTS",
    "Super Shy": "뉴진스",
    "Don't look back in anger": "Oasis",
    "모든 날, 모든 순간": "폴킴",
    "다이너마이트": "BTS"
}

def test(di):
    sample = di
    print(sample)


# 여기에 똑같이 딕셔너리를 인자값으로 넣어줍니다.
def get_song_urls():
    url_list = []
    album_info = get_recommend_songs()
    for song, artist in album_info.items():
        track_query = f"{artist} {song}"
        track_data = search_spotify(track_query, "track", access_token)

        if track_data:
            # print(f"Track Name: {track_data['name']}")
            # print(f"Artist Name: {', '.join(artist['name'] for artist in track_data['artists'])}")
            
            # print(f"Preview URL: {track_data['preview_url']}" if 'preview_url' in track_data else "No preview available")
            url_list.append(track_data['preview_url'])
        else:
            print(f"No results found for '{song}' by '{artist}'")
    return url_list

# print("----url----")
# print(url_list)