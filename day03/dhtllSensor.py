# adafruit_dht 라이브러리를 설치합니다:
# pip install adafruit-circuitpython-dht
# GPIO 라이브러리 의존성을 설치합니다:
# sudo apt install libgpiod2

import time  # 시간 지연을 위한 time 모듈
import adafruit_dht  # DHT11 센서를 제어하는 Adafruit 라이브러리
import board  # 보드의 GPIO 핀 번호를 사용하기 위한 라이브러리

# 📌 DHT11 센서를 사용할 GPIO 핀을 지정 (여기서는 BCM 기준 GPIO 23번 사용)
# board.D23은 라즈베리파이의 GPIO 23번 핀을 의미합니다
dht = adafruit_dht.DHT11(board.D23)

try:
    while True:
        try:
            # 🌡️ 센서로부터 온도 데이터를 읽어옵니다 (섭씨)
            temperature = dht.temperature
            
            # 💧 센서로부터 습도 데이터를 읽어옵니다 (%)
            humidity = dht.humidity

            # 📋 읽어온 온도와 습도를 출력합니다
            print("Temp: {}°C".format(temperature))
            print("Humi: {}%".format(humidity))
            
            # 1초 간격으로 반복 실행
            time.sleep(1)

        except RuntimeError as error:
            # DHT11 센서는 간헐적으로 읽기 오류가 발생하므로
            # RuntimeError가 발생하면 무시하고 다시 시도합니다
            print("Retrying... ({})".format(error.args[0]))
            time.sleep(1)

except KeyboardInterrupt:
    # Ctrl+C 입력 시 루프를 빠져나가며 종료 메시지 출력
    print("프로그램 종료")

finally:
    # 프로그램 종료 시 센서 자원 정리 (일부 버전에서는 생략 가능)
    dht.exit()
