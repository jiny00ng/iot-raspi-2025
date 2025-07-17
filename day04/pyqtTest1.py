import sys 
from PyQt5.QtWidgets import QApplication, QWidget

# MyApp 클래스는 QWidget을 상속받아 새로운 윈도우 창을 정의
class MyApp(QWidget):
    def __init__(self):
        super().__init__()     # 부모 클래스(QWidget)의 초기화 메서드 호출
        self.initUi()          # 사용자 인터페이스 초기화 함수 호출

    # UI 구성 함수 정의
    def initUi(self):
        self.setWindowTitle("My First Application")  # 창 제목 설정
        self.move(300, 300)     # 창의 위치 설정 (x=300, y=300)
        self.resize(400, 200)   # 창의 크기 설정 (너비=400, 높이=200)
        self.show()             # 창을 화면에 표시

# 프로그램이 메인으로 실행될 때만 아래 코드 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성 (이벤트 루프 시작 준비)
    ex = MyApp()                  # MyApp 클래스의 인스턴스 생성 → 창 표시됨
    sys.exit(app.exec_())         # 이벤트 루프 실행 및 종료 시 시스템 종료 처리
