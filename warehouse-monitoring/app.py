# Flask 메인 서버 실행
from flask import Flask, render_template, jsonify, request, redirect, url_for
from db import get_db_connection
from auth import auth_bp, login_required
import sensor, db
import threading
import time

app = Flask(__name__)
app.secret_key = "admin"  # 세션을 위한 비밀 키
app.register_blueprint(auth_bp)

# 임계치 (기본값)
TEMP_THRESHOLD = 30.0
HUM_THRESHOLD = 70.0

# 🔥 추가: 터보 팬 상태를 저장하는 전역 변수 (0: 정지, 1: 작동 중)
# 서버 시작 시 기본값은 '정지'로 설정합니다.
turbo_fan_state = 1 

# 🔥 추가: 터보 팬 GPIO 제어 함수 (sensor.py에 구현되어야 함)
# sensor.py 파일에 control_turbo_fan(state) 함수가 있다고 가정합니다.
# 이 함수는 state 값(0 또는 1)을 받아 터보 팬을 제어합니다.
# 예: sensor.control_turbo_fan(1) -> 터보 팬 켜기, sensor.control_turbo_fan(0) -> 터보 팬 끄기
# 만약 sensor.py에 이 함수가 없다면, 직접 구현해야 합니다 (GPIO 제어 부분).

def background_sensor_task():
    """주기적으로 센서 읽고 DB 저장 + 임계치 경고"""
    while True:
        db = None
        cursor = None
        try:
            db = get_db_connection()
            cursor = db.cursor()
            temperature, humidity = sensor.read_sensor_with_retry()
            if temperature is not None and humidity is not None:
                print(f"Temp: {temperature} °C, Humidity: {humidity} %")
                sql = "INSERT INTO sensor_data (temperature, humidity) VALUES (%s, %s)"
                cursor.execute(sql, (temperature, humidity))
                db.commit()

                if temperature > TEMP_THRESHOLD or humidity > HUM_THRESHOLD:
                    sensor.async_alert(duration=5)
                    sensor.control_fan(temperature, humidity)  # 팬 켜기
                else:
                    sensor.led_green()
                    sensor.control_fan(temperature, humidity)  # 팬 끄기
            else:
                print("Failed to read valid sensor data.")
        except Exception as e:
            print(f"Error in background task: {e}")
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
        time.sleep(5)

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/data")
@login_required
def data():
    global turbo_fan_state # 🔥 추가: 전역 변수 사용 선언
    db = None
    cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT measured_at, temperature, humidity FROM sensor_data ORDER BY id DESC LIMIT 30")
        rows = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching data: {e}")
        rows = []
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    rows.reverse()
    result = []
    for ts, temp, hum in rows:
        alert = 1 if temp > TEMP_THRESHOLD or hum > HUM_THRESHOLD else 0
        fan_status = 1 if temp > TEMP_THRESHOLD or hum > HUM_THRESHOLD else 0  # 팬 ON/OFF
        result.append({
            'time': ts.strftime('%H:%M:%S'),
            'temperature': float(temp),
            'humidity': float(hum),
            'alert': alert,
            'fan': fan_status,
            'turbo_fan': turbo_fan_state # 🔥 추가: 현재 터보 팬 상태를 포함하여 응답
        })

    return jsonify(result)

# 🔥 추가: 터보 팬 제어를 위한 새로운 API 엔드포인트
@app.route("/toggle-turbo-fan", methods=["POST"])
@login_required
def toggle_turbo_fan():
    global turbo_fan_state # 전역 변수 사용 선언

    # 현재 상태를 토글
    turbo_fan_state = 1 - turbo_fan_state # 0이면 1로, 1이면 0으로 변경

    # 🔥 실제 라즈베리파이 GPIO 제어 로직 호출
    # sensor.py 파일에 control_turbo_fan 함수가 있어야 합니다.
    try:
        if hasattr(sensor, 'control_turbo_fan'):
            sensor.control_turbo_fan(turbo_fan_state)
            print(f"터보 팬 상태 변경: {'작동 중' if turbo_fan_state == 1 else '정지'}")
        else:
            print("경고: sensor.control_turbo_fan 함수를 찾을 수 없습니다. 실제 팬 제어가 이루어지지 않습니다.")
            print("sensor.py 파일에 control_turbo_fan(state) 함수를 구현해야 합니다.")
    except Exception as e:
        print(f"터보 팬 제어 중 오류 발생: {e}")
        # 오류 발생 시 상태를 되돌릴지 여부는 앱 로직에 따라 결정
        # turbo_fan_state = 1 - turbo_fan_state 

    return jsonify({"success": True, "turbo_fan_state": turbo_fan_state})


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    global TEMP_THRESHOLD, HUM_THRESHOLD
    if request.method == "POST":
        try:
            TEMP_THRESHOLD = float(request.form["temp_threshold"])
            HUM_THRESHOLD = float(request.form["hum_threshold"])
            print(f"기준치 변경됨 → 온도: {TEMP_THRESHOLD}, 습도: {HUM_THRESHOLD}")
        except ValueError:
            print("잘못된 입력입니다.")
        return redirect(url_for("settings"))

    return render_template("settings.html", temp_threshold=TEMP_THRESHOLD, hum_threshold=HUM_THRESHOLD)

@app.route("/table")
@login_required
def table():
    db = None
    cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT measured_at, temperature, humidity FROM sensor_data ORDER BY id DESC LIMIT 50")
        rows = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching data for table: {e}")
        rows = []
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    rows.reverse()
    return render_template("table.html", data=rows, temp_threshold=TEMP_THRESHOLD, hum_threshold=HUM_THRESHOLD)

if __name__ == "__main__":
    try:
        sensor_thread = threading.Thread(target=background_sensor_task, daemon=True)
        sensor_thread.start()
        app.run(host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        print("서버 종료 중...")
    finally:
        sensor.cleanup()
