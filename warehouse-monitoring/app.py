from flask import Flask, render_template, jsonify, request, redirect, url_for
from db import get_db_connection
from auth import auth_bp, login_required
import sensor, db
import threading
import time

app = Flask(__name__)
app.secret_key = "admin"  # 세션을 위한 비밀 키
app.register_blueprint(auth_bp)

TEMP_THRESHOLD = 30
HUM_THRESHOLD = 70

def background_sensor_task():
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
                else:
                    sensor.led_green()
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
        result.append({
            'time': ts.strftime('%H:%M:%S'),
            'temperature': float(temp),
            'humidity': float(hum),
            'alert': alert
        })

    return jsonify(result)

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
