# event
import sys
from PyQt5.QtWidgets import *

class MyApp(QWidget):
    def __init__(self):
        super().__init__()       # QWidget 초기화
        self.initUi()            # 사용자 UI 설정 함수 호출

    def initUi(self):
        self.setWindowTitle("PyQt Button Test")  # 창 제목 설정
        self.move(300, 300)                      # 창 위치 설정 (x=300, y=300)
        self.resize(400, 200)                    # 창 크기 설정 (너비 400, 높이 200)

        # 버튼 생성: 텍스트는 "click", 부모 위젯은 self
        button = QPushButton("click", self)
        button.move(20, 20)                      # 버튼 위치 설정

        # 버튼 클릭 시 실행할 함수 연결 (시그널-슬롯 연결)
        # 이벤트 핸들러를 connect로 연결
        button.clicked.connect(self.button_clicked)

    # 버튼 클릭 시 호출될 슬롯 함수
    def button_clicked(self):
        # 메시지 박스 표시 (제목: message, 내용: clicked)
        QMessageBox.about(self, "message", "clicked")

# 프로그램 진입점
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성
    ex = MyApp()                  # MyApp 인스턴스 생성 및 UI 표시
    sys.exit(app.exec_())         # 이벤트 루프 시작 및 정상 종료 처리
