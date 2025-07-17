# RPi.GPIO 모듈을 GPIO라는 이름으로 임포트 (라즈베리파이 GPIO 제어용)
import RPi.GPIO as GPIO
# 시간 지연 기능을 위한 time 모듈
import time

# 핀 번호 설정
swPin = 14     # 스위치 입력
ledPin = 18    # LED 연결 출력 핀

# LED 상태 변수 (처음엔 꺼진 상태로 시작)
led_state = False  # False → 꺼짐, True → 켜짐

# GPIO 모드 설정 (BCM 번호 기준 사용)
GPIO.setmode(GPIO.BCM)

# 스위치 핀을 입력으로 설정하고 내부 풀업 저항 활성화
# 풀업(PULL_UP) 설정: 기본적으로 HIGH 상태, 버튼 누르면 GND로 연결되어 LOW 상태가 됨
GPIO.setup(swPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(ledPin, GPIO.OUT)  # LED 출력

# 콜백 함수 정의 - 스위치가 눌릴 때마다 실행됨
# channel 매개변수는 이벤트가 발생한 핀 번호 (자동 전달됨)
def toggle_led(channel):
    global led_state
    led_state = not led_state  # 현재 LED 상태 반전 (토글)
    GPIO.output(ledPin, led_state)  # 반전된 상태를 출력 핀에 적용
    print("LED 상태:", "ON" if led_state else "OFF")    # 상태 출력

# 이벤트 감지 설정
# swPin 핀에서 FALLING(눌렀을 때 LOW로 변할 때) 감지되면 toggle_led 함수 실행
# bouncetime=200 → 200ms 동안 중복 감지 방지 (채터링 방지)
GPIO.add_event_detect(swPin, GPIO.FALLING, callback=toggle_led, bouncetime=200)

try:
    while True:
        time.sleep(0.1)  # 너무 빠르게 돌지 않도록 CPU 사용을 줄이기 위해 대기
except KeyboardInterrupt:
    # Ctrl+C 등으로 프로그램 종료 시 GPIO 리소스를 정리
    print("프로그램 종료")
    GPIO.cleanup()