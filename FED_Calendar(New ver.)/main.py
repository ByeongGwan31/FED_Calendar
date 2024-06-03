import sys
from PyQt5.QtWidgets import QApplication
from calendar_window import CalendarWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CalendarWindow()
    ex.show()
    sys.exit(app.exec_())