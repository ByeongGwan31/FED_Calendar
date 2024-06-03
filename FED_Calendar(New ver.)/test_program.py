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

def main():
    load_dotenv()
    api_key = os.getenv('API_KEY')
    
    while True:
        food_name = input("식품이름을 입력하시오 (종료하려면 'x'를 입력하세요): ")
        if food_name.lower() == 'x':
            print("프로그램을 종료합니다.")
            break

        nutrition_info = get_food_nutrition_info(food_name, api_key)
        
        if nutrition_info:
            print("\n=== 영양 성분 정보 ===")
            print(f"식품명: {nutrition_info['DESC_KOR']}")
            print(f"1회 제공량: {nutrition_info.get('SERVING_WT', 'N/A')} g")
            print(f"열량: {nutrition_info.get('NUTR_CONT1', 'N/A')} kcal")
            print(f"탄수화물: {nutrition_info.get('NUTR_CONT2', 'N/A')} g")
            print(f"단백질: {nutrition_info.get('NUTR_CONT3', 'N/A')} g")
            print(f"지방: {nutrition_info.get('NUTR_CONT4', 'N/A')} g")
            print(f"당류: {nutrition_info.get('NUTR_CONT5', 'N/A')} g")
            print(f"나트륨: {nutrition_info.get('NUTR_CONT6', 'N/A')} mg")
            print(f"콜레스테롤: {nutrition_info.get('NUTR_CONT7', 'N/A')} mg")
            print(f"포화지방산: {nutrition_info.get('NUTR_CONT8', 'N/A')} g")
            print(f"트랜스지방: {nutrition_info.get('NUTR_CONT9', 'N/A')} g")
        else:
            print("해당 식품에 대한 정보를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
