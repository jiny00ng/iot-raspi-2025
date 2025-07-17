from flask import Flask
from gpiozero import LED
import atexit

app = Flask(__name__)
led = LED(21)

atexit.register(led.off)

@app.route('/')
def index():
    return "<h1>LED Control Web</h1>"

@app.route('/led/<state>')
def led_control(state):
    if state == 'on':
        led.on()
    elif state == 'off':
        led.off()
    else:
        return "<h1>Invalid state</h1>", 400
    return f"<h1>LED {state.upper()}</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
