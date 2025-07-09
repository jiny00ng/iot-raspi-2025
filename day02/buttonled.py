import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정 
BUTTON = 17
RED = 14
GREEN = 15
BLUE = 18

# GPIO 모드 설정 (BCM: GPIO 번호 기준)
GPIO.setmode(GPIO.BCM)

# 핀 모드 설정
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # 버튼 입력, 풀업 저항 활성화
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)

# 프로그램 시작 알림: RGB LED 모두 켜서 흰색 출력
GPIO.output(RED, GPIO.HIGH)
GPIO.output(GREEN, GPIO.HIGH)
GPIO.output(BLUE, GPIO.HIGH)

# LED 제어 함수: 인자로 전달된 색상만 켜고 나머지는 끔
def turn_on_led(color):
    GPIO.output(RED, GPIO.HIGH if color == "RED" else GPIO.LOW)
    GPIO.output(GREEN, GPIO.HIGH if color == "GREEN" else GPIO.LOW)
    GPIO.output(BLUE, GPIO.HIGH if color == "BLUE" else GPIO.LOW)

print("버튼을 연속으로 눌러 LED를 제어하세요.")

try:
    while True:
        # 버튼이 눌릴 때까지 대기 (Idle 상태)
        while GPIO.input(BUTTON) == GPIO.HIGH:
            time.sleep(0.01)

        count = 0                          # 연속 누름 횟수 초기화
        last_press_time = time.time()     # 마지막 눌림 시간 기록

        # 연속 입력 감지 루프
        while True:
            # 버튼 눌림 감지
            if GPIO.input(BUTTON) == GPIO.LOW:
                count += 1
                last_press_time = time.time()   # 마지막 눌림 시간 갱신

                # 버튼에서 손 뗄 때까지 대기 (디바운스)
                while GPIO.input(BUTTON) == GPIO.LOW:
                    time.sleep(0.01)

            # 1초 동안 추가 입력이 없으면 루프 종료 (연속 입력 종료로 간주)
            if time.time() - last_press_time > 1.0:
                break

            time.sleep(0.01)

        # 누른 횟수에 따라 LED 색상 제어
        if count == 1:
            color = "OFF"
            turn_on_led("")
        elif count == 2:
            color = "RED"
            turn_on_led("RED")
        elif count == 3:
            color = "GREEN"
            turn_on_led("GREEN")
        elif count == 4:
            color = "BLUE"
            turn_on_led("BLUE")
        else:
            color = "OFF"
            turn_on_led("")

        # 콘솔에 결과 출력
        print(f"감지된 연속 누름 횟수: {count}, LED: {color}")

# 프로그램 종료 시 (Ctrl+C 누르면) GPIO 정리
except KeyboardInterrupt:
    GPIO.cleanup()
