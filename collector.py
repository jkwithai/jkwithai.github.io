import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def collect_naver_news():
    url = "https://news.naver.com/section/101" # 경제 섹션
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 네이버 뉴스 구조에 따라 헤드라인 추출 (구조가 변경될 수 있음에 유의)
        news_list = []
        
        # 최신 뉴스 항목들을 찾습니다. 
        # 네이버 뉴스 섹션의 일반적인 구조인 sa_text_title 클래스를 타겟팅합니다.
        items = soup.select(".sa_text_title")[:10] # 상위 10개 추출
        
        for item in items:
            title = item.get_text(strip=True)
            link = item.get('href')
            if title and link:
                news_list.append({
                    "title": title,
                    "link": link
                })

        # 결과 저장
        data = {
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "news": news_list
        }

        # data 폴더가 없으면 생성
        if not os.path.exists('data'):
            os.makedirs('data')

        with open('data/news.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully collected {len(news_list)} news items.")

    except Exception as e:
        print(f"Error during collection: {e}")

if __name__ == "__main__":
    collect_naver_news()
