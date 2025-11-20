import RPi.GPIO as GPIO

# Settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up LED
GPIO.setup(12, GPIO.OUT)

# Set up buttons
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if GPIO.input(5) == GPIO.LOW or GPIO.input(6) == GPIO.LOW:
        GPIO.output(12, GPIO.HIGH)
    else:
        GPIO.output(12, GPIO.LOW)
