# RPi.GPIO 모듈을 GPIO라는 이름으로 불러오기
import RPi.GPIO as GPIO
# 시간 지연을 위한 time 모듈 불러오기
import time

# 피에조 부저 연결 핀 (BCM 번호 기준)
piezoPin = 17

# 음계 (도~도, 1옥타브) 주파수 리스트 (Hz)
Melody = [262, 294, 330, 349, 392, 440, 494, 523]

# GPIO 번호 모드를 BCM으로 설정
GPIO.setmode(GPIO.BCM)
# 부저 핀을 출력 모드로 설정
GPIO.setup(piezoPin, GPIO.OUT)

# 피에조 부저에 440Hz로 PWM 생성 객체 생성
sound = GPIO.PWM(piezoPin, 440)

try:
    while True:
        sound.start(45)  # 듀티 사이클 50%로 PWM 시작 (소리 재생 시작)
        
        # Melody 리스트에 있는 각 음을 차례로 재생
        for i in range(0, len(Melody)):
            sound.ChangeFrequency(Melody[i])  # 주파수 변경하여 음정 재생
            time.sleep(0.3)  # 각 음을 0.3초 동안 재생
        
        sound.stop()  # PWM 정지 (소리 끔)
        time.sleep(1)  # 1초 대기 후 다시 반복

# Ctrl+C로 종료 시 GPIO 정리
except KeyboardInterrupt:
    GPIO.cleanup()
