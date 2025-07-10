# 가상화경 활성화(env)
# source env/bin/activate 

# adafruit_dht 라이브러리를 설치 (온습도 센서 제어용)
# pip install adafruit-circuitpython-dht

# 라즈베리파이의 GPIO 라이브러리와 의존성 설치
# sudo apt install libgpiod2

import RPi.GPIO as GPIO      # 라즈베리파이 GPIO 제어용 라이브러리
import time                  # 시간 지연을 위한 모듈
import adafruit_dht          # Adafruit에서 제공하는 DHT 센서 제어 라이브러리
import board                 # board.D23 형태로 핀을 지정하기 위한 모듈
import mysql.connector       # 📌 MariaDB 연결용 모듈

# dhtPin = 23                  # 사용할 GPIO 핀 번호 (BCM 기준, GPIO 23번 핀)

GPIO.setmode(GPIO.BCM)       # GPIO 번호 체계를 BCM 모드로 설정

# DHT 라이브러리는 내부에서 핀 설정을 처리하므로 아래 라인은 생략해도 무방
# GPIO.setup(dhtPin, GPIO.IN)

# DHT11 센서를 GPIO 23번 핀에 연결했다고 설정
dht = adafruit_dht.DHT11(board.D23)

# ✅ MariaDB와 연결 설정
try:
    db = mysql.connector.connect(
        host="localhost",
        user="raspi",
        password="raspi",
        database="iotdb"
    )
except mysql.connector.Error as err:
    print("DB 연결 실패:", err)
    exit(1)

# ✅ SQL 실행을 위한 커서 객체 생성
cursor = db.cursor()

try:
    # 무한 반복: 센서 데이터 측정 및 DB 저장
    while True:
        try:
            # 🌡️ 온도 측정 (섭씨)
            temperature = dht.temperature

            # 💧 습도 측정 (퍼센트)
            humidity = dht.humidity

            # 유효한 센서 데이터가 존재하는 경우
            if temperature is not None and humidity is not None:
                print("Temp: ", temperature)
                print("Humi: ", humidity)

                # 📥 DB에 온도 및 습도 데이터 저장
                sql = "INSERT INTO dhtll (temperature, humidity) VALUES (%s, %s)"
                val = (temperature, humidity)
                cursor.execute(sql, val)  # SQL 실행
                db.commit()              # 변경사항 커밋

            else:
                # 센서가 None 값을 반환할 경우
                print("센서에서 유효한 데이터를 읽지 못했습니다.")

            # 1초 대기 후 다음 측정
            time.sleep(1)

        except RuntimeError as error:
            # ⚠️ DHT 센서는 종종 읽기 실패 발생 → 오류 무시하고 다음 루프로 계속
            print("Read error:", error.args[0])
            time.sleep(1)

# 사용자 키보드 인터럽트(Ctrl + C) 감지 시 루프 종료
except KeyboardInterrupt:
    print("측정을 중단합니다.")

# 🔚 종료 시 리소스 정리
finally:
    GPIO.cleanup()     # 사용한 GPIO 핀 초기화
    cursor.close()     # DB 커서 종료
    db.close()         # DB 연결 종료