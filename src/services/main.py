from image_processing import ImageProcessor
from recommend_playlist_songs import SimilaritySearch
from recommend_song_detail import RecommendSongs
import pandas as pd

# 설정 값
model_path = 'src/ml/Vit_model_best_epoch_2.pth'
tag_table_path = 'csv/tag_table3.csv'
song_table_path = 'csv/song_table3.csv'
image_path = 'images/dw2.jpg'


# 이미지 프로세서 인스턴스를 생성합니다.
image_processor = ImageProcessor(model_path=model_path)

# 이미지에서 태그를 추출합니다.
query_tags = image_processor.extract_tags(image_path=image_path)

# 유사성 검색 인스턴스를 생성합니다.
similarity_search = SimilaritySearch(tag_table_path=tag_table_path)

# FAISS 인덱스를 빌드합니다.
similarity_search.build_index()

# 유사한 플레이리스트의 playlist_songs_id를 검색합니다.
similar_playlists_songs_ids = similarity_search.search_similar_playlists(query_tags=query_tags)

# 각 playlist_songs_ids에 대해 get_top_songs을 호출하고 결과를 합칩니다.
all_top_songs = pd.DataFrame()
song_recommender = RecommendSongs(song_table_path=song_table_path)
song_recommender.load_songs()

for playlist_songs_ids_str in similar_playlists_songs_ids:
    top_songs = song_recommender.get_top_songs(playlist_songs_ids_str)
    all_top_songs = pd.concat([all_top_songs, top_songs])

# 중복된 곡을 제거합니다.
all_top_songs.drop_duplicates(inplace=True)

# 전체 top_songs에서 인기도에 따라 상위 5곡을 다시 추출합니다.
all_top_songs = all_top_songs.sort_values(by='popularity', ascending=False).head(5)

# 추천된 곡 정보를 출력합니다.
print(all_top_songs)