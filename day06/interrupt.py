# 라즈베리파이의 GPIO 핀을 제어하기 위한 RPi.GPIO 모듈 불러오기
import RPi.GPIO as GPIO
# 시간 관련 기능 (sleep 등)을 사용하기 위한 time 모듈 불러오기
import time

# 스위치가 연결된 GPIO 핀 번호 (BCM 번호 기준)
swPin = 14

# GPIO 핀 번호 모드를 BCM 방식으로 설정 (실제 GPIO 번호 사용)
GPIO.setmode(GPIO.BCM)

# 해당 핀을 입력으로 설정하고 내부 풀업 저항을 활성화
# 풀업 저항 사용 시 스위치를 누르지 않았을 때는 HIGH, 누르면 GND와 연결되어 LOW 상태가 됩니다.
GPIO.setup(swPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 콜백 함수 정의 - 이벤트 발생 시 호출됨
# channel1은 이벤트가 발생한 핀 번호를 자동으로 전달받음
def printcallback(channel1):
    print("pushed")  # 스위치가 눌렸을 때 출력

# GPIO 이벤트 감지 설정
# RISING: 입력이 LOW → HIGH로 바뀔 때(스위치를 뗄 때) 이벤트 발생
# 콜백 함수로 printcallback을 호출
# 버튼을 누른 후 200ms 이내에 들어오는 중복 이벤트는 무시
GPIO.add_event_detect(swPin, GPIO.RISING, callback=printcallback, bouncetime=200)

try:
    # 프로그램이 종료되지 않도록 무한 루프 유지
    while True:
        pass  # 아무 동작 없이 대기만 함 (이벤트는 백그라운드에서 처리됨)

# Ctrl + C 입력 시 예외 처리
except KeyboardInterrupt:
    # 프로그램 종료 전 GPIO 설정 초기화 (리소스 정리)
    GPIO.cleanup()
