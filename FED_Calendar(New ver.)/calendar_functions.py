import re
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def get_input_with_validation(parent, title, label, regex, error_message):
    while True:
        text, ok = QInputDialog.getText(parent, title, label)
        if not ok:
            return None
        if re.match(regex, text):
            return text
        QMessageBox.warning(parent, "입력 오류", error_message)

def is_valid_date(date_string):
    try:
        QDate.fromString(date_string, "yyyy-MM-dd")
        return True
    except ValueError:
        return False

def displayProductInfo(self, date):
    if date in self.productData:
        info_text = ""
        for idx, (category, product, quantity, manufacture) in enumerate(self.productData[date], 1):
            manufactureDate = QDate.fromString(manufacture, "yyyy-MM-dd").toString('yyyy년 MM월 dd일')
            info_text += f"제조일자: {manufactureDate}<br/>"
            info_text += f"{category} | <b style = 'color:black;'>{product}</b> <b style = 'color:blue;'>{quantity}개</b><br/>"
        info_text += f"<b style = 'color:red;'>⚠️ 유통기한: {date.toString('yyyy년 MM월 dd일')}</b>"
        self.infoLabel.setText(info_text)
        self.infoLabel.setTextFormat(Qt.RichText)
    else:
        self.infoLabel.setText("이 날짜에 등록된 정보가 없습니다.")

def get_food_nutrition_info(food_name, api_key):
    import requests
    url = "http://apis.data.go.kr/1471000/FoodNtrIrdntInfoService1/getFoodNtrItdntList1"
    params = {
        'desc_kor': food_name,
        'pageNo': '1',
        'numOfRows': '100',
        'ServiceKey': api_key,
        'type': 'json'
    }
    response = requests.get(url, params = params)
    
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
