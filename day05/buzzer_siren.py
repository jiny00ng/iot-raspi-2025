import RPi.GPIO as GPIO
import time

# 부저 핀 번호 (BCM 기준)
piezoPin = 17

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(piezoPin, GPIO.OUT)

# PWM 객체 생성 (초기 주파수 100Hz)
sound = GPIO.PWM(piezoPin, 100)

try:
    sound.start(50)  # 듀티 사이클 50%
    while True:
        # ① 주파수 점점 증가 (사이렌 상승음)
        for freq in range(400, 1000, 10):  # 400Hz → 1000Hz
            sound.ChangeFrequency(freq)
            time.sleep(0.005)

        # ② 주파수 점점 감소 (사이렌 하강음)
        for freq in range(1000, 400, -10):  # 1000Hz → 400Hz
            sound.ChangeFrequency(freq)
            time.sleep(0.01)

except KeyboardInterrupt:
    print("사이렌 종료")
    sound.stop()
    GPIO.cleanup()
