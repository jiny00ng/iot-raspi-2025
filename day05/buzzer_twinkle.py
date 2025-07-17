import RPi.GPIO as GPIO
import time

piezoPin = 17

# 도레미파솔라시도 주파수 (4옥타브 기준)
NOTE = {
    'C': 262,
    'D': 294,
    'E': 330,
    'F': 349,
    'G': 392,
    'A': 440,
    'B': 494,
    'c': 523,   # 높은 도
    ' ': 0      # 쉼표
}

# 작은 별 멜로디
melody = ['C', 'C', 'G', 'G', 'A', 'A', 'G', ' ',
          'F', 'F', 'E', 'E', 'D', 'D', 'C', ' ',
          'G', 'G', 'F', 'F', 'E', 'E', 'D', ' ',
          'G', 'G', 'F', 'F', 'E', 'E', 'D', ' ',
          'C', 'C', 'G', 'G', 'A', 'A', 'G', ' ',
          'F', 'F', 'E', 'E', 'D', 'D', 'C']

# 각 음의 길이 (1 = 기본 박자, 0.5 = 반박자)
beats = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5,
         0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 0.5,
         0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 0.5,
         0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 0.5,
         0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 0.5,
         0.5, 0.5, 0.5, 0.5, 0.5, 1, 1]

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(piezoPin, GPIO.OUT)

sound = GPIO.PWM(piezoPin, 440)

try:
    sound.start(45)  # 듀티 사이클 45%
    for i in range(len(melody)):
        note = melody[i]
        beat = beats[i]
        
        freq = NOTE[note]
        
        if freq == 0:
            sound.ChangeDutyCycle(0)  # 쉼표: 소리 끔
        else:
            sound.ChangeFrequency(freq)
            sound.ChangeDutyCycle(45)  # 소리 재생
        
        time.sleep(beat)  # 음 길이만큼 대기
        sound.ChangeDutyCycle(0)  # 음 끝낸 후 잠깐 멈춤
        time.sleep(0.05)

    sound.stop()
    GPIO.cleanup()

except KeyboardInterrupt:
    sound.stop()
    GPIO.cleanup()
