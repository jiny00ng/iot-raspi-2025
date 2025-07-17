import sys
import tty
import termios
import fcntl
import os
import signal
import time
import RPi.GPIO as GPIO

piezoPin = 17
note_freq = {
    '1': 262, '2': 294, '3': 330, '4': 349,
    '5': 392, '6': 440, '7': 494, '8': 523
}

GPIO.setmode(GPIO.BCM)
GPIO.setup(piezoPin, GPIO.OUT)
sound = GPIO.PWM(piezoPin, 440)

running = True

def signal_handler(sig, frame):
    global running
    print("\nCtrl+C 감지 - 종료합니다.")
    running = False

signal.signal(signal.SIGINT, signal_handler)

def set_nonblocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

def main():
    global running
    fd = sys.stdin.fileno()
    old_term = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        set_nonblocking(fd)

        print("숫자 1~8을 누르면 해당 음정이 출력됩니다. (Ctrl+C로 종료)")

        while running:
            try:
                c = sys.stdin.read(1)
            except IOError:
                c = None
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt - 종료합니다.")
                break

            if c is None or c == '':
                time.sleep(0.01)
                continue

            if c in ['\n', '\r']:
                continue

            if c in note_freq:
                freq = note_freq[c]
                print(f"입력: {c} → 주파수: {freq}Hz", flush=True)
                sound.start(50)
                sound.ChangeFrequency(freq)
                time.sleep(0.15)
                sound.stop()
            else:
                print(f"'{c}'는 1~8 숫자가 아닙니다.", flush=True)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_term)
        sound.stop()
        GPIO.cleanup()
        print("GPIO 정리 완료, 프로그램 종료")

if __name__ == "__main__":
    main()
