# 📅 식품 유통기한 관리 시스템

---

## 프로젝트 목적 🎯

본 프로젝트의 목적은 식품 판매업자가 식품의 유통기한을 효과적으로 관리할 수 있고, 식품을 구매한 구매자도 효율적으로 유통기한을 알 수 있는 도구를 제공하는 것입니다. 유통기한이 임박한 식품을 식별하고 관리하는 과정을 자동화하여 식품 폐기를 줄일 수 있고, 운영 효율성을 증가시키는 것을 목표로 합니다.

## 프로젝트 내용 📋

본 프로젝트는 달력을 표시하고, 사용자가 식품의 유통기한, 카테고리, 물품명, 수량을 입력할 수 있도록 합니다. GUI 기반 어플리케이션으로 작성되었으며, 입력된 데이터는 지정된 날짜에 표시가 되어, 사용자가 입력한 식품들의 정보를 확인 가능합니다. 이를 위해 PyQt5의 QCalendarWidget 라이브러리를 사용하였으며, 다양한 유용한 라이브러리도 활용하였습니다.

또한, 식품 의약안전처의 식품 영양성분 DB API를 활용하여 사용자가 입력한 식품의 영양 성분을 표시할 수 있도록 할 것입니다. 사용자가 입력한 데이터는 CSV 파일에 저장되어 프로그램 종료 후에도 데이터를 유지하고, 캘린더에서 조회가 가능합니다.

## 기대효과 및 활용 방안 🌟

본 프로젝트의 기대 효과는 다음과 같습니다:
1. **유통기한 관리 효율성 증가**: 시각적 달력을 통해 유통기한이 임박한 식품을 쉽게 식별 가능합니다.
2. **비용 절감**: 임박한 유통기한을 확인하고, 폐기되는 식품의 양을 줄임으로써 비용을 절감할 수 있습니다.
3. **재고 관리 최적화**: 시스템을 통해 정확한 유통기한 정보를 기반으로 재고를 더 효과적으로 관리할 수 있습니다.
4. **프로모션 전략**: 유통기한이 임박한 제품을 식별함으로써 특정 제품에 대한 할인이나 프로모션을 진행하여 시기적절하게 계획할 수 있습니다. 재고 회전율을 증가시키고, 수익성을 향상 시킬 수 있습니다.
5. **데이터 활용**: 식품영양성분 DB API를 활용하여, 영양 정보를 효과적으로 제공할 수 있습니다.
6. **실시간 데이터 관리**: 입력된 데이터는 프로그램 종료 시 초기화되는 것이 아닌, CSV 파일에 자동으로 저장되어 읽기, 쓰기, 불러오기를 할 수 있으며, 프로그램 종료 후에도 데이터가 유지되며 캘린더에서 바로 조회가 가능합니다.

## 참고 문헌 📚

1. 어준, 파이썬 달력 만들기 (Naver – Blog, August 7, 2019) [링크](https://blog.naver.com/euijun54/221608433531)
2. 박응용, 점프 투 파이썬 – 라이브러리 예제 편, 17장 기타서비스 다루기, 106 그래픽 사용자 인터페이스를 만들려면? [링크](https://wikidocs.net/132610)
3. 대학원생 개발자의 일상 (Tistory, October 20, 2023) [링크](https://gr-st-dev.tistory.com/1965)
4. Docs Python org, tkinter – Python interface to Tcl/TK [링크](https://docs.python.org/ko/3/library/tkinter.html)
5. 최애가 최애, Python : calendar – 달력 관련 라이브러리 (Tistory – January 21, 2021) [링크](https://chae-developer.tistory.com/23)
6. Truman Show, 파이썬(Python) - 날짜 / 달력 관련 라이브러리 (Tistory – February 25, 2020) [링크](https://truman.tistory.com/81)
7. 식품의약품안전처 공공데이터 활용, 식품영양성분 DB(New). 링크
8. 초보자를 위한 Python GUI 프로그래밍, 02. 위젯과 레이아웃, 02.14. Display – QCalendarWidget [링크](https://wikidocs.net/38036)
9. Youtube – Fun With Code. Creating calendar in Python || PyQt QCalendarWidget [링크](https://www.youtube.com/watch?v=hvyEb7LhPYs)
10. Youtube – Geeks Coders – PyQt5 튜토리얼 – QCalendarWidget으로 달력을 만드는 방법 [링크](https://www.youtube.com/watch?v=NlO_dYbwr5c)
11. Youtube – Code First with hala – PyQt5 Daily Task Planning app #2: QCalendarWidget [링크](https://www.youtube.com/watch?v=GcBv-dmHq5M)
12. Docs Python org, re – Regular expression operations [링크](https://docs.python.org/3/library/re.html)
13. StackOverflow – Include Scripts from Feature folder in ScriptBundle [링크](https://stackoverflow.com/questions/48196214/include-scripts-from-feature-folder-in-scriptbundle/48199672#48199672)
14. StackOverflow – JQuery; Declare duplicate global values in [링크](https://stackoverflow.com/questions/37517714/jquery-declare-duplicate-global-values-in/37517759#37517759)

## 사전 준비 ⚙️

1. **Python 3.x 설치**
    - [Python 다운로드 페이지](https://www.python.org/downloads/)에서 최신 버전을 다운로드하여 설치합니다.

2. **필요한 라이브러리 설치**
    - 아래 명령어를 통해 필요한 라이브러리를 설치합니다:
    ```sh
    pip install PyQt5 pandas matplotlib
    ```

## 실행 방법 ▶️

프로그램이 실행되면 다음과 같은 주요 기능을 수행할 수 있는 버튼들이 제공됩니다:

### 1. 제품 입력
- **기능**: 사용자가 선택한 날짜에 새로운 식품 정보를 입력할 수 있습니다.
- **사용 방법**: 
    1. 달력에서 유통기한을 입력할 날짜를 클릭합니다.
    2. "제품 입력" 버튼을 클릭합니다.
    3. 팝업 창에서 카테고리, 물품명, 개수, 제조일자, 유통기한을 입력합니다.
    4. 확인을 클릭하여 데이터를 저장합니다.

### 2. 제품 삭제
- **기능**: 선택한 날짜의 특정 제품 정보를 삭제할 수 있습니다.
- **사용 방법**:
    1. 달력에서 삭제할 제품이 있는 날짜를 클릭합니다.
    2. "제품 삭제" 버튼을 클릭합니다.
    3. 팝업 창에서 삭제할 제품을 선택합니다.
    4. 확인을 클릭하여 제품을 삭제합니다.

### 3. 모든 제품 조회
- **기능**: 현재 저장된 모든 제품 정보를 조회할 수 있습니다.
- **사용 방법**:
    1. "모든 제품 조회" 버튼을 클릭합니다.
    2. 팝업 창에서 모든 제품의 유통기한, 카테고리, 물품명, 개수, 제조일자 정보를 확인할 수 있습니다.

### 4. 그래프 보기
- **기능**: 카테고리별로 제품의 개수를 그래프로 확인할 수 있습니다.
- **사용 방법**:
    1. "그래프 보기" 버튼을 클릭합니다.
    2. 팝업 창에서 카테고리별 제품 개수 그래프를 확인할 수 있습니다.

### 5. 날짜 클릭 시 제품 정보 조회
- **기능**: 선택한 날짜의 제품 정보를 조회할 수 있습니다.
- **사용 방법**:
    1. 달력에서 정보를 조회할 날짜를 클릭합니다.
    2. 선택한 날짜에 저장된 제품 정보를 하단의 레이블에서 확인할 수 있습니다.



## 파일 설명 📂

- `main.py`: 메인 프로그램 파일. `CalendarWindow` 클래스를 실행합니다.
- `calendar_window.py`: 캘린더 창 클래스 파일. 캘린더와 GUI 요소들을 정의합니다.
- `calendar_functions.py`: 캘린더 기능을 포함한 파일. 날짜 유효성 검사, 입력 검증 등의 함수들을 포함합니다.
- `product_data.csv`: 프로그램에서 사용하는 데이터 파일. 사용자가 입력한 식품 정보가 저장됩니다.

## 폴더 구조 📁

- **FED_Calendar(Old ver.)**: 모듈화하기 전의 구 버전 코드가 포함된 폴더입니다.
- **FED_Calendar(New ver.)**: 현재 개발 중인 프로젝트 폴더입니다. 이 폴더는 모듈화된 최신 버전의 코드를 포함하고 있으며, 2024년 06월 09일 이전으로 개발 완료될 예정입니다.
---
