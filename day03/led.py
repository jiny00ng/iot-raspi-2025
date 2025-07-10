import RPi.GPIO as GPIO
import time

# BCM mode 설정
GPIO.setmode(GPIO.BCM)

# RGB 핀 번호 설정
RED = 14
GREEN = 15
BLUE = 18

# pin mode 설정
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)

# 출력값 설정
try:
	while True:
		# RED ON
		GPIO.output(RED, GPIO.HIGH)
		GPIO.output(GREEN, GPIO.LOW)
		GPIO.output(BLUE, GPIO.LOW)
		time.sleep(2)

		# GREEN ON
		GPIO.output(RED,GPIO.LOW)
		GPIO.output(GREEN, GPIO.HIGH)
		GPIO.output(BLUE, GPIO.LOW)
		time.sleep(2)	

		# BLUE ON
		GPIO.output(RED,GPIO.LOW)
		GPIO.output(GREEN, GPIO.LOW)
		GPIO.output(BLUE, GPIO.HIGH)
		time.sleep(2)

except KeyboardInterrupt:
	GPIO.cleanup()
