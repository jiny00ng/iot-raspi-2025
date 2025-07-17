import sys
from PyQt5.QtWidgets import *

# QApplication 객체 생성
# → PyQt5 애플리케이션은 반드시 하나의 QApplication 인스턴스가 필요함
app = QApplication(sys.argv)

# QPushButton 위젯 생성 (텍스트는 "Quit")
# → 버튼이 하나 생기며, "Quit"이라는 텍스트가 표시됨
# label = QLabel("Hello PyQt!")  # 라벨 대신 버튼을 사용 중
label = QPushButton("Quit")

# 위젯을 화면에 표시
label.show()

# 이벤트 루프 실행
# → GUI가 사용자 이벤트(클릭 등)를 받을 수 있도록 무한 루프에 진입
app.exec()