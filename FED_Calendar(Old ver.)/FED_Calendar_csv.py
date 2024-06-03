import sys
import re
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager, rc
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont, QColor, QTextCharFormat
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QPushButton, QVBoxLayout, QWidget, QLabel, QInputDialog, QMessageBox, QDialog, QVBoxLayout, QTextEdit

font_path = "C:/Windows/Fonts/malgun.ttf" 
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

class CalendarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.productData = {}
        self.csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'product_data.csv')
        self.load_data()

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumDate(QDate(2022, 1, 1))
        self.calendar.setMaximumDate(QDate(2027, 12, 31))
        self.layout.addWidget(self.calendar)
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
        self.btnShowGraphs = QPushButton("그래프 보기", self)
        self.btnShowGraphs.clicked.connect(self.showGraphs)
        self.layout.addWidget(self.btnShowGraphs)
        self.setGeometry(300, 300, 1400, 800)
        self.setWindowTitle('식품 관리 캘린더')
        self.calendar.clicked.connect(self.calendarClicked)

    def is_valid_date(self, date_str):
        try:
            date = QDate.fromString(date_str, "yyyy-MM-dd")
            if not date.isValid():
                return False
            year = date.year()
            month = date.month()
            day = date.day()
            if not (2022 <= year <= 2027):
                return False
            if not (1 <= month <= 12):
                return False
            if day > QDate(year, month, 1).daysInMonth():
                return False
            return True
        except:
            return False

    def get_input_with_validation(self, title, label, pattern, error_msg, previous_value=""):
        while True:
            input_dialog = QInputDialog(self)
            input_dialog.setWindowFlags(input_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
            value, ok = input_dialog.getText(self, title, label, text=previous_value)
            if not ok:
                return None
            if re.match(pattern, value) and self.is_valid_date(value):
                return value
            QMessageBox.warning(self, "입력 오류", error_msg)

    def load_data(self):
        try:
            df = pd.read_csv(self.csv_file_path, encoding='euc-kr')
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
        df.to_csv(self.csv_file_path, index=False, encoding='euc-kr')

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

        manufacture = self.get_input_with_validation(
            "알림!", 
            "제조일자 혹은 구매 날짜를 입력하시오 (YYYY-MM-DD)",
            r'^\d{4}-\d{2}-\d{2}$',
            "제조일자는 2022-2026년 범위 내에서 yyyy-mm-dd 형식으로 입력해주세요."
        )
        if not manufacture:
            return

        expiry = self.get_input_with_validation(
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
                                    f"제품명: <b>{product}</b> | 수량: <b style='color:blue;'>{quantity}</b> 개<br>")

        product_texts = []
        for date, entries in sorted(products.items()):
            date_text = f"<b>유통기한: <b style='color:red;'>{date.toString('yyyy년 MM월 dd일')}</b></b><br>"
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

    def updateDateTextFormat(self, date):
        if date in self.productData:
            format = QTextCharFormat()
            format.setForeground(QColor('purple'))
            format.setFontWeight(QFont.Bold)
            self.calendar.setDateTextFormat(date, format)
        else:
            self.calendar.setDateTextFormat(date, QTextCharFormat())

    def calendarClicked(self, date):
        self.displayProductInfo(date)

    def displayProductInfo(self, date):
        if date in self.productData:
            info_text = ""
            for idx, (category, product, quantity, manufacture) in enumerate(self.productData[date], 1):
                manufactureDate = QDate.fromString(manufacture, "yyyy-MM-dd").toString('yyyy년 MM월 dd일')
                info_text += f"제조일자: {manufactureDate}<br/>"
                info_text += f"{category} | <b style='color:black;'>{product}</b> <b style='color:blue;'>{quantity}개</b><br/>"
            info_text += f"<b style='color:red;'>⚠️ 유통기한: {date.toString('yyyy년 MM월 dd일')}</b>"
            self.infoLabel.setText(info_text)
            self.infoLabel.setTextFormat(Qt.RichText)
        else:
            self.infoLabel.setText("이 날짜에 등록된 정보가 없습니다.")

    def showGraphs(self):
        df = pd.read_csv(self.csv_file_path, encoding='euc-kr')

        categories = df['카테고리'].unique()
        colors = plt.cm.tab20(np.linspace(0, 1, len(categories)))
        color_map = {category: color for category, color in zip(categories, colors)}

        fig, ax = plt.subplots(figsize=(20, 10))

        category_counts = df['카테고리'].value_counts()
        bars = ax.bar(category_counts.index, category_counts.values, color=[color_map[cat] for cat in category_counts.index])
        
        ax.set_title('카테고리별 제품 개수', fontsize=20)
        ax.set_xlabel('카테고리', fontsize=15)
        ax.set_ylabel('개수', fontsize=15)
        
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom', fontsize=12)
        
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        
        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CalendarWindow()
    ex.show()
    sys.exit(app.exec_())
