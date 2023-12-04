from .image_processing import ImageProcessor
from .recommend_playlist_songs import SimilaritySearch
from .recommend_song_detail import RecommendSongs
import pandas as pd
import sys, os
import json 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from ..utils import image_module
from settings.path import *

def get_filtered_tags(tags_list, min_count):
    """
    입력된 모든 태그 리스트에서 min_count보다 크거나 같은 값을 가지는 태그들을 추출합니다.
    """
    # 모든 태그 리스트를 합산합니다.
    sum_of_tags = [0] * len(tags_list[0])
    for tags in tags_list:
        sum_of_tags = [sum_value + tag for sum_value, tag in zip(sum_of_tags, tags)]

    # min_count보다 크거나 같은 태그만 필터링합니다.
    filtered_tags = [1 if count >= min_count else 0 for count in sum_of_tags]
    return filtered_tags

def get_recommend_songs():
    # 이미지 프로세서 인스턴스를 생성합니다.
    image_processor = ImageProcessor(model_path=MODEL_PATH)
    
    #file = [image.filename for image in images]
    # 이미지의 경로를 정의합니다. 여러개 가능
    
    #image_paths = [IMG_PATH+"/image_1.jpg", IMG_PATH+"/image_2.jpg", IMG_PATH+"/image_3.jpg"]
    image_paths = image_module.to_list()
    
    # 각 이미지의 태그를 추출합니다.
    extracted_tags = [image_processor.extract_tags(image_path=image_path) for image_path in image_paths]

    # 입력된 이미지 개수 / 2보다 크거나 같은 값을 가진 태그들만 필터링합니다. 입력 이미지 개수가 홀수일경우 반올림
    min_count = round(len(image_paths) / 2)
    filtered_query_tags = get_filtered_tags(extracted_tags, min_count)

    # class_idx_to_label JSON 파일을 로드합니다.
    with open(IDX_JSON_PATH, 'r', encoding='utf-8') as json_file:
        class_idx_to_label = json.load(json_file)

    # 태그를 레이블로 매핑합니다.
    filtered_query_labels = [class_idx_to_label[str(idx)] for idx, value in enumerate(filtered_query_tags) if value == 1]

    # 유사성 검색 인스턴스를 생성합니다.
    similarity_search = SimilaritySearch(tag_table_path=TAG_TABLE_PATH)

    # FAISS 인덱스를 빌드합니다.
    similarity_search.build_index()

    # 유사한 플레이리스트의 playlist_songs_id를 검색합니다.
    similar_playlists_songs_ids = similarity_search.search_similar_playlists(query_tags=filtered_query_tags)

    # 각 playlist_songs_ids에 대해 get_top_songs을 호출하고 결과를 합칩니다.
    all_top_songs = pd.DataFrame()
    song_recommender = RecommendSongs(song_table_path=SONG_TABLE_PATH)
    song_recommender.load_songs()

    for playlist_songs_ids_str in similar_playlists_songs_ids:
        top_songs = song_recommender.get_top_songs(playlist_songs_ids_str)
        all_top_songs = pd.concat([all_top_songs, top_songs])

    # 중복된 곡을 제거합니다.
    all_top_songs.drop_duplicates(inplace=True)

    # 전체 top_songs에서 인기도에 따라 상위 5곡을 다시 추출합니다.
    all_top_songs = all_top_songs.sort_values(by='popularity', ascending=False).head(5)
    
    # 곡 제목과 아티스트 이름으로 구성된 딕셔너리 생성
    songs_dict = {row['SONG_TITLE']: row['ARTIST_NAME'] for _, row in all_top_songs.iterrows()}

    # 추천된 곡 정보를 출력합니다.
    # print(songs_dict)
    # print(filtered_query_tags)
    # print(filtered_query_labels)
    # print(all_top_songs)
    #print(songs_dict)
    return songs_dict