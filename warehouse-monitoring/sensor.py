# ================================
# 📦 센서 및 하드웨어 제어 모듈
# ================================
import board
import adafruit_dht
from gpiozero import LED, OutputDevice
from time import sleep, time
import threading
import RPi.GPIO as GPIO # 🔥 추가: RPi.GPIO 라이브러리 임포트 (gpiozero와 함께 사용 가능)

# -------------------------
# 🌡️ DHT11 센서 초기화 (GPIO4 핀 사용)
# -------------------------
dht = adafruit_dht.DHT11(board.D4)

# -------------------------
# 💡 LED 초기화 (GPIO 번호)
# 빨강(17), 파랑(22), 초록(27)
# -------------------------
red_led = LED(17)
blue_led = LED(22)
green_led = LED(27)

# -------------------------
# 🔊 부저 초기화 (GPIO18 핀)
# -------------------------
buzzer = LED(18)

# 🌀 쿨링팬(릴레이) 초기화 (GPIO23)
# active_high=True → on() 시 전원 공급
fan_relay = OutputDevice(23, active_high=True, initial_value=False)

# 🔥 추가: 터보 팬(릴레이) 초기화 (예시: GPIO1 핀)
# active_high=True → on() 시 전원 공급 (릴레이가 HIGH 신호에 활성화된다고 가정)
# 만약 릴레이가 LOW 신호에서 활성화되는 'active_low' 타입이라면 active_high=False로 설정
TURBO_FAN_GPIO_PIN = 1 # 🔥 실제 라즈베리파이에 연결된 GPIO 핀 번호로 변경하세요.
turbo_fan_relay = OutputDevice(TURBO_FAN_GPIO_PIN, active_high=True, initial_value=False)

# -------------------------
# ✅ 정상 상태 (초록 LED 켜기)
# -------------------------
def led_green():
    green_led.on()
    red_led.off()
    blue_led.off()

# -------------------------
# 🚨 경고 상태 (빨강/파랑 번갈아 점멸)
# duration: 깜빡이는 시간(초)
# -------------------------
def led_red_blue_blink(duration=5):
    end_time = time() + duration
    while time() < end_time:
        red_led.on()
        blue_led.off()
        green_led.off()
        sleep(0.5)
        red_led.off()
        blue_led.on()
        sleep(0.5)
    # 종료 후 LED 끄기
    red_led.off()
    blue_led.off()

# -------------------------
# 🔊 부저 경고음
# beep_count: 울리는 횟수
# beep_duration: 켜져 있는 시간
# pause_duration: 끄는 시간
# -------------------------
def buzzer_alert(beep_count=5, beep_duration=0.3, pause_duration=0.3):
    for _ in range(beep_count):
        buzzer.on()    # 부저 켜기
        sleep(beep_duration)
        buzzer.off()   # 부저 끄기
        sleep(pause_duration)

# -------------------------
# 🌡️ 센서 데이터 읽기 (재시도 기능 포함)
# retry: 읽기 실패 시 몇 번 다시 시도할지
# -------------------------
def read_sensor_with_retry(retry=3):
    for _ in range(retry):
        try:
            temperature = dht.temperature
            humidity = dht.humidity
            if temperature is not None and humidity is not None:
                return round(temperature, 1), round(humidity, 1)
        except RuntimeError as e:
            print(f"DHT read error: {e}")
        sleep(1)
    return None, None

# 🌀 팬 제어 (온습도 임계치 기반)
TEMP_THRESHOLD = 30     # 섭씨
HUMIDITY_THRESHOLD = 70 # %

def control_fan(temperature, humidity):
    if temperature > TEMP_THRESHOLD or humidity > HUMIDITY_THRESHOLD:
        fan_relay.on()   # 팬 켜기
    else:
        fan_relay.off()  # 팬 끄기

# 🔥 추가: 터보 팬 제어 함수
def control_turbo_fan(state):
    """
    터보 팬을 제어합니다.
    state: 0 (정지), 1 (작동)
    """
    if state == 1:
        turbo_fan_relay.on() # 터보 팬 켜기
        print("터보 팬 ON")
    else:
        turbo_fan_relay.off() # 터보 팬 끄기
        print("터보 팬 OFF")

# -------------------------
# 🚨 비동기 경고 알림
# LED 점멸 + 부저 울림을 동시에 실행
# -------------------------
def async_alert(duration=5):
    def alert_task():
        led_red_blue_blink(duration)
        buzzer_alert()
        led_green()  # 종료 후 정상 상태 복귀
    threading.Thread(target=alert_task, daemon=True).start()

# -------------------------
# 🧹 종료 시 GPIO 정리
# -------------------------
def cleanup():
    print("센서 및 GPIO 정리...")
    dht.exit()
    red_led.off()
    blue_led.off()
    green_led.off()
    buzzer.off()
    fan_relay.off()   # 기존 팬 릴레이 끄기
    turbo_fan_relay.off() # 🔥 추가: 터보 팬 릴레이 끄기
    GPIO.cleanup() # gpiozero를 사용하더라도 RPi.GPIO를 직접 임포트했기 때문에 호출 권장
