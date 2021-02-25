import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import random

# 몽고DB
client = MongoClient(host="localhost", port=27017)
# myweb 데이터베이스
db = client.myweb
# board 컬렉션
col = db.board

# 검색 결과의 5페이지까지만 수집
for i in range(70):
    	# 게시물 작성시간 기록을 위해 현재시간 저장 (utc 타임)
        current_utc_time = round(datetime.utcnow().timestamp() * 1000)

        try:
        	# 검색 결과의 제목은 h3 태그의 LC20lb 클래스에 있음
            title = f"title = {i}"

            # 검색결과의 요약내용은 div 태그의 s 클래스에 있음
            contents = f"contents = {i} 이야기"

            # 몽고DB에 저장
            # 작성자와 writer_id 설정 필요
            col.insert_one({
                "name": "테스터",
                "writer_id": "",
                "title": title,
                "contents": contents,
                "view": 0,
                "pubdate": current_utc_time
            })
        except:
            pass