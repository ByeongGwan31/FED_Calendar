import requests
from dotenv import load_dotenv
import os

def get_food_nutrition_info(food_name, api_key):
    url = "http://apis.data.go.kr/1471000/FoodNtrIrdntInfoService1/getFoodNtrItdntList1"
    params = {
        'desc_kor': food_name,
        'pageNo': '1',
        'numOfRows': '100',
        'ServiceKey': api_key,
        'type': 'json'
    }
    response = requests.get(url, params=params)
    
    print(f"HTTP 상태 코드: {response.status_code}")
    print(f"응답 내용: {response.text[:200]}...")
    
    try:
        data = response.json()
        if 'body' in data and 'items' in data['body'] and data['body']['items']:
            items = data['body']['items']
            filtered_items = [item for item in items if item['DESC_KOR'].split(',')[0].strip() == food_name]
            if filtered_items:
                return filtered_items[0]
            else:
                return None
        else:
            return None
    except ValueError:
        print("응답 오류")
        return None
