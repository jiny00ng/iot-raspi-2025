# 시스템 관련 모듈 임포트
import sys

# PyQt5 위젯 관련 모듈
from PyQt5.QtWidgets import *

# .ui 파일을 불러오기 위한 PyQt 모듈
from PyQt5 import uic

# 라즈베리파이 GPIO 제어 모듈
import RPi.GPIO as GPIO

# -----------------------------------------------------------
# Qt Designer로 만든 UI 파일 불러오기 (.ui 파일명: ledButton.ui)
# loadUiType은 (폼 클래스, 베이스 클래스)를 튜플로 반환하므로 [0]으로 첫 번째만 가져옴
form_class = uic.loadUiType("ledButton.ui")[0]

# -----------------------------------------------------------
# GPIO 핀 설정 (BCM 모드 기준)
RED = 14
GREEN = 15
BLUE = 18

# -----------------------------------------------------------
# 메인 윈도우 클래스 정의 - QDialog와 form_class(UI) 상속
class WindowClass(QDialog, form_class):
    def __init__(self):
        super().__init__()        # 부모 클래스 초기화
        self.setupUi(self)        # UI 초기화 (Qt Designer 위젯을 객체에 바인딩)
        self.setupGPIO()          # GPIO 초기 설정
        self.updateLabel("All OFF")  # 프로그램 시작 시 텍스트 표시

    # -------------------------------------------------------
    # GPIO 설정 함수
    def setupGPIO(self):
        GPIO.setmode(GPIO.BCM)       # GPIO 핀 넘버링을 BCM 모드로 설정
        GPIO.setwarnings(False)      # 경고 메시지 비활성화
        GPIO.setup(RED, GPIO.OUT)    # 핀들을 출력 모드로 설정
        GPIO.setup(GREEN, GPIO.OUT)
        GPIO.setup(BLUE, GPIO.OUT)
        # 모든 LED 끄기
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW)

    # -------------------------------------------------------
    # QLabel에 상태 메시지를 출력하는 함수
    def updateLabel(self, message):
        self.textLabel.setText(message)  # textLabel은 Qt Designer에서 만든 QLabel 객체 이름

    # -------------------------------------------------------
    # Red 버튼 클릭 시 실행되는 슬롯 함수
    def slot1(self):
        print("Red ON")
        GPIO.output(RED, GPIO.HIGH)   # 빨간 LED 켜기
        GPIO.output(GREEN, GPIO.LOW)  # 나머지 끄기
        GPIO.output(BLUE, GPIO.LOW)
        self.updateLabel("Red LED ON")  # 상태 표시

    # Green 버튼 클릭 시
    def slot2(self):
        print("Green ON")
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.LOW)
        self.updateLabel("Green LED ON")

    # Blue 버튼 클릭 시
    def slot3(self):
        print("Blue ON")
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.HIGH)
        self.updateLabel("Blue LED ON")

    # OFF 버튼 클릭 시 (모든 LED 끄기)
    def slot4(self):
        print("All OFF")
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW)
        self.updateLabel("All LED OFF")

    # -------------------------------------------------------
    # 창 닫힐 때 실행되는 종료 이벤트: GPIO 정리
    def closeEvent(self, event):
        GPIO.cleanup()    # GPIO 핀 정리 (자원 반환)
        event.accept()    # 창 닫기 허용

# -----------------------------------------------------------
# 프로그램 시작 부분
if __name__ == "__main__":
    app = QApplication(sys.argv)     # QApplication 객체 생성 (필수)
    myWindow = WindowClass()         # 사용자 정의 창 클래스 생성
    myWindow.show()                  # 창 띄우기
    sys.exit(app.exec_())            # 이벤트 루프 실행 및 종료 코드 반환
