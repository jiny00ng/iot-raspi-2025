from flask import Flask        # Flask 웹 서버 프레임워크 import
import RPi.GPIO as GPIO       # 라즈베리파이 GPIO 제어 라이브러리 import

# Flask 애플리케이션 객체 생성
app = Flask(__name__)         # '__name__'은 현재 실행 중인 모듈 이름을 의미

# LED 제어에 사용할 GPIO 핀 번호 (BCM 번호 기준)
ledPin = 21

# GPIO 설정
GPIO.setmode(GPIO.BCM)        # BCM 핀 번호 체계 사용
GPIO.setup(ledPin, GPIO.OUT)  # ledPin 핀을 출력 모드로 설정

# 기본 페이지 ('/') 요청 시 실행될 함수
@app.route('/')
def helloflask():
    return "Hello Flask"      # 웹 브라우저에 표시될 문자열

# '/led/on' 요청 시 LED를 켜는 함수
@app.route('/led/on')
def led_on():
    GPIO.output(ledPin, GPIO.HIGH)  # GPIO 21번 핀에 HIGH 출력 (LED ON)
    return "<h1>LED ON</h1>"        # 브라우저에 표시할 메시지

# '/led/off' 요청 시 LED를 끄는 함수
@app.route('/led/off')
def led_off():
    GPIO.output(ledPin, GPIO.LOW)   # GPIO 21번 핀에 LOW 출력 (LED OFF)
    return "<h1>LED OFF</h1>"       # 브라우저에 표시할 메시지

# 웹서버 시작 (0.0.0.0은 외부 접속 허용, 포트 8080 사용)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
