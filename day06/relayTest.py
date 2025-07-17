# RPi.GPIO 모듈을 GPIO라는 이름으로 가져옵니다 (라즈베리파이의 GPIO 핀 제어용)
import RPi.GPIO as GPIO
# 시간 지연을 위한 time 모듈 가져오기
import time

# 릴레이가 연결된 GPIO 핀 번호 (BCM 번호 기준)
relayPin = 18

# GPIO 핀 번호 체계를 BCM 방식으로 설정 (GPIO 번호 사용)
GPIO.setmode(GPIO.BCM)

# 릴레이 핀을 출력 모드로 설정
GPIO.setup(relayPin, GPIO.OUT)

try:
    # 무한 반복 실행
    while True:
        # 릴레이 핀에 HIGH 신호 출력 (릴레이 ON)
        GPIO.output(relayPin, True)
        print("True")  # 상태 출력
        time.sleep(1)  # 1초 대기

        # 릴레이 핀에 LOW 신호 출력 (릴레이 OFF)
        GPIO.output(relayPin, False)
        print("False")  # 상태 출력
        time.sleep(1)  # 1초 대기

# 사용자가 Ctrl+C로 프로그램을 종료할 때 예외 처리
except KeyboardInterrupt:
    print("bye~~")  # 종료 메시지 출력

# 프로그램 종료 시 GPIO 설정 초기화 (핀 해제)
finally:
    GPIO.cleanup()
