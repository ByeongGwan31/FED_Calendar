import os
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from calendar_functions import *

class CalendarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.productData = {}
        self.csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'product_data.csv')
        self.load_data()

    def initUI(self):
        self.setWindowTitle('식품 관리 캘린더')
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'FED_Icon', 'FED_Icon.ico')
        self.setWindowIcon(QIcon(icon_path))

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        self.calendarLayout = QHBoxLayout()
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumDate(QDate(2022, 1, 1))
        self.calendar.setMaximumDate(QDate(2027, 12, 31))
        self.calendarLayout.addWidget(self.calendar)
        self.calendar.clicked.connect(self.calendarClicked)

        self.rightLayout = QVBoxLayout()

        # 년도 선택 레이아웃
        self.yearLayout = QVBoxLayout()
        self.cmbYearSelect = QComboBox(self)
        self.cmbYearSelect.addItem("년도 선택", -1)
        for year in range(2022, 2028):
            self.cmbYearSelect.addItem(f"{year}년", year)
        self.cmbYearSelect.currentIndexChanged.connect(self.yearSelected)
        self.yearLayout.addWidget(self.cmbYearSelect)
        self.rightLayout.addLayout(self.yearLayout)

        # 월 선택 레이아웃
        self.headLayout = QVBoxLayout()
        self.cmbMonthSelect = QComboBox(self)
        self.cmbMonthSelect.addItem("월 선택", -1)
        for month in range(1, 13):
            self.cmbMonthSelect.addItem(f"{month}월", month)
        self.cmbMonthSelect.currentIndexChanged.connect(self.monthSelected)
        self.headLayout.addWidget(self.cmbMonthSelect)
        self.monthInfoLabel = QTextEdit(self)
        self.monthInfoLabel.setReadOnly(True)
        self.headLayout.addWidget(self.monthInfoLabel)
        self.headLayout.setStretch(0, 1)
        self.headLayout.setStretch(1, 6)
        self.rightLayout.addLayout(self.headLayout)

        # 영양성분 검색 레이아웃
        self.tailLayout = QVBoxLayout()
        self.btnSearchNutrition = QPushButton("영양성분 검색", self)
        self.btnSearchNutrition.clicked.connect(self.searchNutrition)
        self.tailLayout.addWidget(self.btnSearchNutrition)
        self.nutritionInfoLabel = QTextEdit(self)
        self.nutritionInfoLabel.setReadOnly(True)
        self.tailLayout.addWidget(self.nutritionInfoLabel)

        self.warningLabel = QLabel("⚠️ 제품의 이름을 정확히 입력히 입력하세요.<br>⚠️ 식품 성분 DB를 조회하는거라 검색한 정보가 없을수도 있습니다.", self)
        self.warningLabel.setStyleSheet("color: red;")
        self.tailLayout.addWidget(self.warningLabel)
        
        self.tailLayout.setStretch(0, 1)
        self.tailLayout.setStretch(1, 4)
        self.rightLayout.addLayout(self.tailLayout)

        self.rightLayout.setStretch(0, 1)  # 년 선택 레이아웃 조정
        self.rightLayout.setStretch(1, 6)  # 월 검색 레이아웃 조정
        self.rightLayout.setStretch(2, 4)  # 영양성분 검색

        self.calendarLayout.addLayout(self.rightLayout)
        self.layout.addLayout(self.calendarLayout)

        self.infoLabel = QLabel("제품을 입력해주세요", self)
        self.layout.addWidget(self.infoLabel)

        self.btnAddInfo = QPushButton("제품 입력", self)
        self.btnAddInfo.clicked.connect(self.addProductInfo)
        self.layout.addWidget(self.btnAddInfo)

        self.btnDeleteInfo = QPushButton("제품 삭제", self)
        self.btnDeleteInfo.clicked.connect(self.deleteProductInfo)
        self.layout.addWidget(self.btnDeleteInfo)

        self.btnViewAll = QPushButton("모든 제품 조회", self)
        self.btnViewAll.clicked.connect(self.viewAllProducts)
        self.layout.addWidget(self.btnViewAll)

        self.btnGoToday = QPushButton("오늘 날짜로 이동", self)
        self.btnGoToday.clicked.connect(self.goToday)
        self.layout.addWidget(self.btnGoToday)

        screen = QGuiApplication.primaryScreen().geometry()
        width, height = screen.width(), screen.height()
        window_width, window_height = int(width * 0.9), int(height * 0.8)  # 창 크기 조정
        left = int((width - window_width) / 2)
        top = int((height - window_height) / 2)
        self.setGeometry(left, top, window_width, window_height)

        self.highlightToday()

    def load_data(self):
        try:
            df = pd.read_csv(self.csv_file_path, encoding = 'euc-kr')
            for _, row in df.iterrows():
                expiryDate = QDate.fromString(row['유통기한'], 'yyyy-MM-dd')
                if expiryDate not in self.productData:
                    self.productData[expiryDate] = []
                self.productData[expiryDate].append([
                    row['카테고리'],
                    row['물품명'],
                    row['개수'],
                    row['제조일자']
                ])
                self.updateDateTextFormat(expiryDate)
        except FileNotFoundError:
            pass

    def save_data(self):
        data = []
        for date, entries in self.productData.items():
            for entry in entries:
                data.append({
                    '카테고리': entry[0],
                    '물품명': entry[1],
                    '개수': entry[2],
                    '제조일자': entry[3],
                    '유통기한': date.toString('yyyy-MM-dd')
                })
        df = pd.DataFrame(data)
        df.to_csv(self.csv_file_path, index = False, encoding = 'euc-kr')

    def addProductInfo(self):
        date = self.calendar.selectedDate()
        category, ok = QInputDialog.getText(self, "알림!", "카테고리를 입력하시오")
        if not ok:
            return

        product, ok = QInputDialog.getText(self, "알림!", "물품명을 입력하시오")
        if not ok:
            return

        quantity, ok = QInputDialog.getInt(self, "알림!", "개수를 입력하시오 (숫자만 가능)")
        if not ok:
            return

        manufacture = get_input_with_validation(
            self,
            "알림!", 
            "제조일자 혹은 구매 날짜를 입력하시오 (YYYY-MM-DD)",
            r'^\d{4}-\d{2}-\d{2}$',
            "제조일자는 2022-2026년 범위 내에서 yyyy-mm-dd 형식으로 입력해주세요."
        )
        if not manufacture:
            return

        expiry = get_input_with_validation(
            self,
            "알림!", 
            "유통기한을 입력하시오 (YYYY-MM-DD)",
            r'^\d{4}-\d{2}-\d{2}$',
            "유통기한은 2022-2027년 범위 내에서 yyyy-mm-dd 형식으로 입력해주세요."
        )
        if not expiry:
            return
        
        expiryDate = QDate.fromString(expiry, "yyyy-MM-dd")
        if expiryDate.isValid():
            if expiryDate not in self.productData:
                self.productData[expiryDate] = []
            found = False
            for item in self.productData[expiryDate]:
                if item[:3] == (category, product, manufacture):
                    item[2] += quantity
                    found = True
                    break
            if not found:
                self.productData[expiryDate].append([category, product, quantity, manufacture])
            self.updateDateTextFormat(expiryDate)
            self.calendar.update()
            self.save_data()
            self.highlightToday()  # 오늘 날짜 강조 유지
        else:
            QMessageBox.warning(self, "알림!", "유효한 유통기한을 입력해주세요.")

    def deleteProductInfo(self):
        date = self.calendar.selectedDate()
        if date in self.productData:
            items = []
            for idx, prod in enumerate(self.productData[date]):
                item = f"{idx + 1}. {prod[1]} ({prod[0]}, {prod[2]}개)"
                items.append(item)
            item, ok = QInputDialog.getItem(self, "제품 삭제", "삭제할 제품을 선택하세요:", items, 0, False)
            if ok and item:
                index = int(item.split('.')[0]) - 1
                del self.productData[date][index]
                QMessageBox.information(self, "제품 삭제", "제품이 삭제되었습니다.")
                if not self.productData[date]:
                    del self.productData[date]
                self.updateDateTextFormat(date)
                self.calendar.update()
                self.save_data()
                self.highlightToday()  # 오늘 날짜 강조 유지
        else:
            QMessageBox.information(self, "제품 삭제", "이 날짜에 등록된 제품이 없습니다.")

    def viewAllProducts(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("모든 유통기한 조회")
        layout = QVBoxLayout()
    
        titleLabel = QLabel("<h2>모든 제품 정보</h2>")
        layout.addWidget(titleLabel)

        textEdit = QTextEdit()
        textEdit.setReadOnly(True)
        products = {}

        for date, entries in sorted(self.productData.items()):
            if date not in products:
                products[date] = []
            for category, product, quantity, manufacture in entries:
                manufactureDate = QDate.fromString(manufacture, "yyyy-MM-dd").toString('yyyy년 MM월 dd일')
                products[date].append(f"제조일자: {manufactureDate} | 카테고리: <b>{category}</b><br>"
                                    f"제품명: <b>{product}</b> | 수량: <b style = 'color:blue;'>{quantity}</b> 개<br>")

        product_texts = []
        for date, entries in sorted(products.items()):
            date_text = f"<b>유통기한: <b style = 'color:red;'>{date.toString('yyyy년 MM월 dd일')}</b></b><br>"
            entries_text = "<br>".join(entries)
            product_texts.append(f"{date_text}{entries_text}<br><br>")

        textEdit.setHtml("<br>".join(product_texts))
        layout.addWidget(textEdit)

        closeButton = QPushButton("닫기")
        closeButton.clicked.connect(dialog.close)
        layout.addWidget(closeButton)

        dialog.setLayout(layout)
        dialog.resize(800, 600)
        dialog.exec_()

    def calendarClicked(self, date):
        displayProductInfo(self, date)

    def searchNutrition(self):
        food_name, ok = QInputDialog.getText(self, "영양성분 검색", "성분 검색 (정확한 이름 입력):")
        if not ok or not food_name:
            return
        
        api_key = os.getenv('API_KEY')
        nutrition_info = get_food_nutrition_info(food_name, api_key)
        
        if nutrition_info:
            nutrition_text = (
                f"<b>식품명:</b> {nutrition_info['DESC_KOR']}<br>"
                f"<b>1회 제공량:</b> <span style = 'color:blue;'>{nutrition_info.get('SERVING_WT', 'N/A')}</span> g<br>"
                f"<b>열량:</b> <span style = 'color:blue;'>{nutrition_info.get('NUTR_CONT1', 'N/A')}</span> kcal<br>"
                f"<b>탄수화물:</b> <span style = 'color:blue;'>{nutrition_info.get('NUTR_CONT2', 'N/A')}</span> g<br>"
                f"<b>단백질:</b> <span style = 'color:blue;'>{nutrition_info.get('NUTR_CONT3', 'N/A')}</span> g<br>"
                f"<b>지방:</b> <span style = 'color:blue;'>{nutrition_info.get('NUTR_CONT4', 'N/A')}</span> g<br>"
                f"<b>당류:</b> <span style = 'color:blue;'>{nutrition_info.get('NUTR_CONT5', 'N/A')}</span> g<br>"
                f"<b>나트륨:</b> <span style = 'color:blue;'>{nutrition_info.get('NUTR_CONT6', 'N/A')}</span> mg<br>"
                f"<b>콜레스테롤:</b> <span style = 'color:blue;'>{nutrition_info.get('NUTR_CONT7', 'N/A')}</span> mg<br>"
                f"<b>포화지방산:</b> <span style = 'color:blue;'>{nutrition_info.get('NUTR_CONT8', 'N/A')}</span> g<br>"
                f"<b>트랜스지방:</b> <span style = 'color:blue;'>{nutrition_info.get('NUTR_CONT9', 'N/A')}</span> g"
            )
            self.nutritionInfoLabel.setHtml(nutrition_text)
        else:
            self.nutritionInfoLabel.setText("해당 식품에 대한 정보를 찾을 수 없습니다.")

    def yearSelected(self, index):
        year = self.cmbYearSelect.itemData(index)
        self.calendar.setSelectedDate(QDate(year, self.calendar.selectedDate().month(), 1))

    def monthSelected(self, index):
        if index == 0:
            return

        month = self.cmbMonthSelect.itemData(index)
        self.monthInfoLabel.clear()
        products = {}

        for date, entries in self.productData.items():
            if date.year() == self.calendar.selectedDate().year() and date.month() == month:
                if date not in products:
                    products[date] = []
                for category, product, quantity, manufacture in entries:
                    manufactureDate = QDate.fromString(manufacture, "yyyy-MM-dd").toString('yyyy년 MM월 dd일')
                    products[date].append(f"제조일자: {manufactureDate} | 카테고리: <b>{category}</b><br>"
                                        f"제품명: <b>{product}</b> | 수량: <b style = 'color:blue;'>{quantity}</b> 개<br>")

        product_texts = []
        for date, entries in sorted(products.items()):
            date_text = f"<b>유통기한: <b style = 'color:red;'>{date.toString('yyyy년 MM월 dd일')}</b></b><br>"
            entries_text = "<br>".join(entries)
            product_texts.append(f"{date_text}{entries_text}<br><br>")

        self.monthInfoLabel.setHtml("<br>".join(product_texts))

        first_day_of_month = QDate(self.calendar.selectedDate().year(), month, 1)
        self.calendar.setSelectedDate(first_day_of_month)
        self.calendar.showSelectedDate()

    def goToday(self):
        today = QDate.currentDate()
        self.calendar.setSelectedDate(today)
        self.highlightToday()

    def highlightToday(self):
        today = QDate.currentDate()
        format = QTextCharFormat()
        format.setBackground(QBrush(QColor("#A4E9F5")))  # 파랑색 배경
        self.calendar.setDateTextFormat(today, format)

    def updateDateTextFormat(self, date):
        format = QTextCharFormat()
        if date in self.productData:
            format.setBackground(QBrush(QColor("#F1F1F1")))  # 일정 배경색
        self.calendar.setDateTextFormat(date, format)
        self.highlightToday()

if __name__ == "__main__":
    app = QApplication([])
    ex = CalendarWindow()
    ex.show()
    app.exec_()
