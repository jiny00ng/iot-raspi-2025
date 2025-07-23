# 센서 및 하드웨어 제어 모듈
import board
import adafruit_dht
from gpiozero import LED
from time import sleep, time
import threading

# 센서 초기화 (DHT11: GPIO4)
dht = adafruit_dht.DHT11(board.D4)

# LED 초기화
red_led = LED(17)
blue_led = LED(22)
green_led = LED(27)

# 부저 (PWM 제어용 GPIO 18)
buzzer = LED(18)

def led_green():
    green_led.on()
    red_led.off()
    blue_led.off()

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
    red_led.off()
    blue_led.off()

def buzzer_alert(beep_count=5, beep_duration=0.3, pause_duration=0.3):
    for _ in range(beep_count):
        buzzer.on()    # 부저 켜기
        sleep(beep_duration)
        buzzer.off()   # 부저 끄기
        sleep(pause_duration)

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

def async_alert(duration=5):
    def alert_task():
        led_red_blue_blink(duration)
        buzzer_alert()   # 함수 이름 맞춤
        led_green()
    threading.Thread(target=alert_task, daemon=True).start()

def cleanup():
    dht.exit()
    red_led.off()
    blue_led.off()
    green_led.off()
    buzzer.off()
