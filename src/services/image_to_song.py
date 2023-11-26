from .image_processing import ImageProcessor
from .recommend_playlist_songs import SimilaritySearch
from .recommend_song_detail import RecommendSongs
import pandas as pd
import sys, os
import json 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from settings import path

def get_common_tags(tags_list):
    #입력된 모든 태그 리스트에 대해 or 연산을 수행합니다.
    common_tags = tags_list[0]
    for tags in tags_list[1:]:
        common_tags = [a or b for a, b in zip(common_tags, tags)] 
    return common_tags

def get_recommend_songs():
    # 이미지 프로세서 인스턴스를 생성합니다.
    image_processor = ImageProcessor(model_path=path.MODEL_PATH)
    
    # 이미지의 경로를 정의합니다. 여러개 가능
    image_paths = [path.IMG_PATH+"/image_1.jpg", path.IMG_PATH+"/image_2.jpg"]

    # 각 이미지의 태그를 추출합니다.
    extracted_tags = [image_processor.extract_tags(image_path=image_path) for image_path in image_paths]

    # 입력된 모든 이미지의 태그에 대해 공통 태그를 찾습니다.
    common_query_tags = get_common_tags(extracted_tags)
    
    # class_idx_to_label JSON 파일을 로드합니다.
    with open(path.IDX_JSON_PATH, 'r', encoding='utf-8') as json_file:
        class_idx_to_label = json.load(json_file)

    # 태그를 레이블로 매핑합니다.
    common_query_labels = [class_idx_to_label[str(idx)] for idx, value in enumerate(common_query_tags) if value == 1]

    # 유사성 검색 인스턴스를 생성합니다.
    similarity_search = SimilaritySearch(tag_table_path=path.TAG_TABLE_PATH)

    # FAISS 인덱스를 빌드합니다.
    similarity_search.build_index()

    # 유사한 플레이리스트의 playlist_songs_id를 검색합니다.
    similar_playlists_songs_ids = similarity_search.search_similar_playlists(query_tags=common_query_tags)

    # 각 playlist_songs_ids에 대해 get_top_songs을 호출하고 결과를 합칩니다.
    all_top_songs = pd.DataFrame()
    song_recommender = RecommendSongs(song_table_path=path.SONG_TABLE_PATH)
    song_recommender.load_songs()

    for playlist_songs_ids_str in similar_playlists_songs_ids:
        top_songs = song_recommender.get_top_songs(playlist_songs_ids_str)
        all_top_songs = pd.concat([all_top_songs, top_songs])

    # 중복된 곡을 제거합니다.
    all_top_songs.drop_duplicates(inplace=True)

    # 전체 top_songs에서 인기도에 따라 상위 5곡을 다시 추출합니다.
    all_top_songs = all_top_songs.sort_values(by='popularity', ascending=False).head(5)

    # 추천된 곡 정보를 출력합니다.
    print(common_query_tags)
    print(common_query_labels)
    print(all_top_songs)
