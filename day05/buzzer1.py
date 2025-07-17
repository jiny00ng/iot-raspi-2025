# RPi.GPIO 모듈을 GPIO라는 이름으로 불러오기
import RPi.GPIO as GPIO
# 시간 지연을 위한 time 모듈 불러오기
import time

# 부저를 연결한 GPIO 핀 번호 (BCM 기준)
buzzerPin = 18

# GPIO 핀 번호 모드를 BCM으로 설정 (GPIO 번호 기준)
GPIO.setmode(GPIO.BCM)
# 부저 핀을 출력 모드로 설정
GPIO.setup(buzzerPin, GPIO.OUT)

try:
    # 부저 켜기 (HIGH 출력)
    GPIO.output(buzzerPin, GPIO.HIGH)
    print("Buzzer On")
    
    # 1초 대기
    time.sleep(1)
    
    # 부저 끄기 (LOW 출력)
    GPIO.output(buzzerPin, GPIO.LOW)
    print("Buzzer Off")

# 사용자가 Ctrl+C로 실행을 중단했을 때 처리
except KeyboardInterrupt:
    print("end...")

# 프로그램 종료 시 GPIO 설정 초기화
finally:
    GPIO.cleanup()
