## 사이렌 + RGB LED 깜빡임 + 버튼

# 필요한 모듈 불러오기
import RPi.GPIO as GPIO
import time

# 핀 설정 (BCM 번호 기준)
piezoPin = 17        # 피에조 부저 핀
buttonPin = 27       # 버튼 입력 핀
redPin = 14          # RGB LED 빨강
greenPin = 15        # RGB LED 초록 (이번 코드에서는 사용 X)
bluePin = 18         # RGB LED 파랑

# GPIO 초기화
GPIO.setmode(GPIO.BCM)                          # BCM 핀 번호 체계 사용
GPIO.setup(piezoPin, GPIO.OUT)                  # 부저 핀 출력 설정
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 버튼 입력 (풀업 저항 사용)
GPIO.setup(redPin, GPIO.OUT)                    # RGB LED 빨강 출력 설정
GPIO.setup(greenPin, GPIO.OUT)                  # RGB LED 초록 출력 설정 (미사용)
GPIO.setup(bluePin, GPIO.OUT)                   # RGB LED 파랑 출력 설정

# PWM 객체 생성 (주파수 100Hz, 추후 변경 가능)
sound = GPIO.PWM(piezoPin, 100)

# 사이렌 작동 여부를 저장하는 상태 변수
melody_active = False

# 버튼 눌림을 감지하는 함수 (디바운싱 처리 포함)
def is_button_pressed():
    if GPIO.input(buttonPin) == GPIO.LOW:        # 버튼 눌림은 LOW 상태
        time.sleep(0.02)                         # 채터링 방지를 위한 짧은 대기
        if GPIO.input(buttonPin) == GPIO.LOW:    # 여전히 눌린 상태면
            while GPIO.input(buttonPin) == GPIO.LOW:  # 버튼에서 손 뗄 때까지 대기
                time.sleep(0.01)
            return True                          # 정상 눌림 반환
    return False                                 # 아니면 False

# 모든 RGB LED를 끄는 함수
def led_off():
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.LOW)

# 메인 프로그램 실행
try:
    print("버튼을 눌러 사이렌 + RGB LED를 켜고/끄세요.")

    while True:
        # 버튼이 눌렸을 경우 사이렌 상태 토글
        if is_button_pressed():
            melody_active = not melody_active

            if melody_active:
                print("사이렌 ON")
                sound.start(50)  # 부저 시작 (듀티 사이클 50%)
            else:
                print("사이렌 OFF")
                sound.stop()
                led_off()        # LED도 끄기

        # 사이렌이 활성화되었을 때 부저와 RGB LED 작동
        while melody_active:
            # 상승음: 400Hz → 1000Hz (빨간 LED 깜빡임)
            for freq in range(400, 1000, 10):
                if is_button_pressed():           # 루프 중 버튼 다시 눌림 감지
                    melody_active = False
                    sound.stop()
                    led_off()
                    print("사이렌 OFF")
                    break
                sound.ChangeFrequency(freq)       # 주파수 변경
                GPIO.output(redPin, GPIO.HIGH)    # 빨간색 ON
                time.sleep(0.0025)
                GPIO.output(redPin, GPIO.LOW)     # 빨간색 OFF
                time.sleep(0.0025)

            if not melody_active:
                break

            # 하강음: 1000Hz → 400Hz (파란 LED 깜빡임)
            for freq in range(1000, 400, -10):
                if is_button_pressed():
                    melody_active = False
                    sound.stop()
                    led_off()
                    print("사이렌 OFF")
                    break
                sound.ChangeFrequency(freq)
                GPIO.output(bluePin, GPIO.HIGH)   # 파란색 ON
                time.sleep(0.0025)
                GPIO.output(bluePin, GPIO.LOW)    # 파란색 OFF
                time.sleep(0.0025)

# Ctrl+C로 종료 시 정리 작업
except KeyboardInterrupt:
    print("종료 중...")
    sound.stop()
    led_off()
    GPIO.cleanup()
