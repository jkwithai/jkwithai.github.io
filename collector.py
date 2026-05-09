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

def collect_bizinfo_news():
    # 서울(6110000), 경기(6410000) 지원사업 목록 페이지
    # URL 파라미터를 통해 지역 필터링이 된 상태로 요청
    url = "https://www.bizinfo.go.kr/sii/siia/selectSIIA200View.do?schAreaDetailCodes=6110000,6410000"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        biz_list = []
        # 테이블의 모든 행을 가져옵니다.
        items = soup.select("table tbody tr")
        
        for item in items:
            # 제목 링크 추출 (보통 3번째 열)
            link_tag = item.select_one("td:nth-child(3) a") or item.select_one("td.txt_left a")
            if not link_tag:
                continue
                
            title = link_tag.get_text(strip=True)
            relative_link = link_tag.get('href', '')
            
            # 링크가 JavaScript 호출인 경우나 빈 경우 처리
            if not relative_link or 'javascript' in relative_link:
                # 상세 페이지 ID가 있다면 추출 로직이 필요할 수 있음
                # 여기서는 일단 URL 구성을 시도
                link = "https://www.bizinfo.go.kr/sii/siia/selectSIIA200View.do" 
            else:
                link = f"https://www.bizinfo.go.kr{relative_link}" if relative_link.startswith('/') else relative_link
            
            # 신청 기간 추출 (보통 4번째 열)
            tds = item.select("td")
            period = tds[3].get_text(strip=True) if len(tds) > 3 else "상세확인"
            
            biz_list.append({
                "title": title,
                "link": link,
                "period": period
            })

        # 상위 10개만 유지
        biz_list = biz_list[:10]

        data = {
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": biz_list
        }

        # 결과 저장
        with open('data/bizinfo.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully collected {len(biz_list)} bizinfo items.")

    except Exception as e:
        print(f"Error during bizinfo collection: {e}")

def get_outfit_recommendation(temp):
    if temp < 5:
        return "패딩, 두꺼운 코트, 목도리, 기모제품"
    elif 5 <= temp < 9:
        return "코트, 가죽 자켓, 히트텍, 니트, 레깅스"
    elif 9 <= temp < 12:
        return "자켓, 트렌치코트, 야상, 니트, 청바지"
    elif 12 <= temp < 17:
        return "자켓, 가디건, 야상, 스타킹, 청바지, 면바지"
    elif 17 <= temp < 20:
        return "얇은 니트, 맨투맨, 가디건, 청바지"
    elif 20 <= temp < 23:
        return "긴팔 티, 가디건, 후드티, 면바지, 슬랙스"
    elif 23 <= temp < 28:
        return "반팔, 얇은 셔츠, 반바지, 면바지"
    else:
        return "민소매, 반팔, 반바지, 원피스"

def collect_weather_and_outfit():
    # 서울 좌표 (Lat: 37.5665, Lon: 126.9780)
    url = "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current_weather=true&timezone=Asia%2FSeoul"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        
        current = weather_data.get("current_weather", {})
        temp = current.get("temperature")
        weather_code = current.get("weathercode")
        
        # 날씨 코드에 따른 텍스트 (WMO Code 기준)
        weather_desc = {
            0: "맑음", 1: "대체로 맑음", 2: "구름 조금", 3: "흐림",
            45: "안개", 48: "안개", 51: "가랑비", 53: "가랑비", 55: "가랑비",
            61: "비", 63: "비", 65: "강한 비", 71: "눈", 73: "눈", 75: "강한 눈",
            95: "뇌우"
        }
        
        desc = weather_desc.get(weather_code, "정보 없음")
        outfit = get_outfit_recommendation(temp)
        
        data = {
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temp": temp,
            "description": desc,
            "outfit": outfit,
            "code": weather_code
        }
        
        with open('data/weather.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"Successfully collected weather: {temp}°C, {desc}")
        
    except Exception as e:
        print(f"Error during weather collection: {e}")

if __name__ == "__main__":
    collect_naver_news()
    collect_bizinfo_news()
    collect_weather_and_outfit()
