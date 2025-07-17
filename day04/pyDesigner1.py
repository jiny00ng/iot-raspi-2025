import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic  # .ui 파일을 불러오기 위한 모듈

# QDialog를 상속받은 사용자 정의 클래스 생성
class WindwoClass(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)  # 부모 클래스 초기화
        self.ui = uic.loadUi("design1.ui", self)  # Qt Designer에서 만든 UI 파일 로드
        self.ui.show()  # UI를 화면에 표시 (보통 QDialog에서는 self.show()도 사용 가능)

    # Qt Designer에서 연결한 슬롯 이름 (clicked() → slot1()으로 연결됨)
    def slot1(self): 
        print("Bye Byes~~")  # 버튼 클릭 시 출력될 메시지

# 프로그램 실행 시작 지점
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성 (필수)
    myWindow = WindwoClass()      # 사용자 정의 다이얼로그 창 생성 및 UI 적용
    app.exec_()                   # 이벤트 루프 실행 (GUI 대기 상태 유지)
