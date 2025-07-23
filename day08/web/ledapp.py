from flask import Flask, request, render_template
# Flask: 웹 서버 프레임워크
# request: 사용자의 요청 데이터 처리
# render_template: HTML 파일을 렌더링할 때 사용

from gpiozero import LED  # gpiozero: Raspberry Pi의 GPIO를 간단하게 제어하는 라이브러리

app = Flask(__name__)  # Flask 애플리케이션 객체 생성

led = LED(21)  # GPIO21(BCM 모드)에 연결된 LED 객체 생성 → 해당 핀에 LED 연결 필요

@app.route('/')
def home():
    # 웹 브라우저에서 '/' 주소로 접속 시 index.html 페이지 반환
    return render_template("index.html")

@app.route('/data', methods=['POST'])
def control():
    data = request.form['led']  # HTML 폼에서 전송된 'led' 값 ('on' 또는 'off')을 가져옴
    if data == 'on':
        led.on()   # 'on'이면 LED 켜기
    else:
        led.off()  # 'off'이면 LED 끄기
    return render_template("index.html")  # 다시 index.html 페이지 반환

if __name__ == '__main__':
    # 이 파일이 메인으로 실행될 때 Flask 서버 실행
    # host='0.0.0.0' → 외부에서도 접속 가능
    # port=5000 → 접속 주소는 http://라즈베리파이IP:5000
    # debug=False → 디버그 모드 끔
    app.run(host='0.0.0.0', port=5000, debug=False)
