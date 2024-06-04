import sys
import os
from PyQt5.QtWidgets import *
from calendar_window import *
from dotenv import load_dotenv

def main():
    load_dotenv()
    app = QApplication(sys.argv)
    ex = CalendarWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
