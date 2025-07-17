from flask import Flask
import gpiod
import atexit

app = Flask(__name__)

# Raspberry Pi 5에서 사용할 GPIO 칩 이름 (환경에 따라 다를 수 있음)
CHIP_NAME = 'gpiochip4'

# 제어할 RGB LED 핀 번호 (BCM 기준)
pins = {
    'r': 20,  # 빨간 LED 핀
    'g': 21,  # 초록 LED 핀
    'b': 16   # 파란 LED 핀
}

# GPIO 칩 열기
chip = gpiod.Chip(CHIP_NAME)

# 각 색깔별 GPIO 라인 객체를 저장할 딕셔너리
lines = {}

# 각 핀을 출력용으로 요청하고 lines 딕셔너리에 저장
for color, pin in pins.items():
    line = chip.get_line(pin)
    line.request(consumer=f"flask-rgb-{color}", type=gpiod.LINE_REQ_DIR_OUT)
    lines[color] = line

# 프로그램 종료 시 모든 LED 끄고 GPIO 자원 해제하는 함수
def cleanup():
    for line in lines.values():
        line.set_value(0)  # LED OFF
        line.release()     # 라인 해제
    chip.close()          # 칩 닫기

# 프로그램 종료 시 cleanup 함수 자동 호출 등록
atexit.register(cleanup)

# 기본 루트 경로: 간단한 안내 메시지
@app.route('/')
def index():
    return """
    <h1>RGB LED Control</h1>
    <p>/led/&lt;color&gt;/&lt;state&gt; 에서 제어하세요.</p>
    <p>color: r, g, b</p>
    <p>state: on, off</p>
    <p>예) /led/r/on</p>
    <p>/led/off_all 으로 모두 끌 수 있습니다.</p>
    """

# 색상과 상태에 따라 해당 LED 켜고 끄는 라우트
@app.route('/led/<color>/<state>')
def led_control(color, state):
    color = color.lower()  # 소문자로 변환
    state = state.lower()

    # 색상 값 검증
    if color not in lines:
        return "<h1>Invalid color</h1>", 400

    # 상태 값 검증
    if state not in ('on', 'off'):
        return "<h1>Invalid state</h1>", 400

    line = lines[color]
    line.set_value(1 if state == 'on' else 0)  # LED ON/OFF 제어
    return f"<h1>LED {color.upper()} {state.upper()}</h1>"

# 모든 LED를 한꺼번에 끄는 라우트
@app.route('/led/off_all')
def off_all():
    for line in lines.values():
        line.set_value(0)  # 모든 LED 끄기
    return "<h1>All LEDs OFF</h1>"

# 메인 함수: Flask 앱 실행
if __name__ == "__main__":
    app.run(host='0.0.0.0')  # 외부 접속 허용, 기본 포트 5000번
