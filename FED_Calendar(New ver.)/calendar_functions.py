import re
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat, QColor, QFont
from PyQt5.QtWidgets import QInputDialog, QMessageBox

def is_valid_date(date_str):
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

def get_input_with_validation(self, title, label, pattern, error_msg, previous_value = ""):
    while True:
        input_dialog = QInputDialog(self)
        input_dialog.setWindowFlags(input_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        value, ok = input_dialog.getText(self, title, label, text=previous_value)
        if not ok:
            return None
        if re.match(pattern, value) and is_valid_date(value):
            return value
        QMessageBox.warning(self, "입력 오류", error_msg)

def updateDateTextFormat(calendar, date, productData):
    if date in productData:
        format = QTextCharFormat()
        format.setForeground(QColor('purple'))
        format.setFontWeight(QFont.Bold)
        calendar.setDateTextFormat(date, format)
    else:
        calendar.setDateTextFormat(date, QTextCharFormat())

def displayProductInfo(self, date, productData, infoLabel):
    if date in productData:
        info_text = ""
        for idx, (category, product, quantity, manufacture) in enumerate(productData[date], 1):
            manufactureDate = QDate.fromString(manufacture, "yyyy-MM-dd").toString('yyyy년 MM월 dd일')
            info_text += f"제조일자: {manufactureDate}<br/>"
            info_text += f"{category} | <b style = 'color:black;'>{product}</b> <b style = 'color:blue;'>{quantity}개</b><br/>"
        info_text += f"<b style = 'color:red;'>⚠️ 유통기한: {date.toString('yyyy년 MM월 dd일')}</b>"
        infoLabel.setText(info_text)
        infoLabel.setTextFormat(Qt.RichText)
    else:
        infoLabel.setText("이 날짜에 등록된 정보가 없습니다.")
