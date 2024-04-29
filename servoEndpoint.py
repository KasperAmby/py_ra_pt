from flask import Flask, request
import RPi.GPIO as GPIO
import time
import board
import neopixel

# Cleanup GPIO settings and setup GPIO mode
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

# Setup for first servo on pin 11
GPIO.setup(17, GPIO.OUT)
servo = GPIO.PWM(17, 50)
servo.start(0)

# Setup for second servo on pin 12
GPIO.setup(27, GPIO.OUT)
servo1 = GPIO.PWM(27, 50)
servo1.start(0)

print("Turning back to 0 degrees")
servo.ChangeDutyCycle(2)
servo1.ChangeDutyCycle(2)

servo.ChangeDutyCycle(0)
servo1.ChangeDutyCycle(0)

#Initialise a strips variable, provide the GPIO Data Pin
#utilised and the amount of LED Nodes on strip and brightness (0 to 1 value)
pixels1 = neopixel.NeoPixel(board.D21, 15, brightness=0.5)

pixels1.fill((0, 220, 0))

#LED Node 10 and colour Blue was selected
pixels1[10] = (0, 20, 255)


app = Flask(__name__)

@app.route('/post', methods=['POST'])
def handle_post():
    ser0 = request.form.get('servo0')
    ser1 = request.form.get('servo1')
    response_messages = []

    try:
        if ser0 is not None:
            ser0 = int(ser0)  # Konverterer ser0 til et heltal
            servo.ChangeDutyCycle(ser0)
            response_messages.append(f"Rotating servo0 to angle: {ser0}")
        
        if ser1 is not None:
            ser1 = int(ser1)  # Konverterer ser1 til et heltal
            servo1.ChangeDutyCycle(ser1)
            response_messages.append(f"Rotating servo1 to angle: {ser1}")
    except ValueError:
        return "Invalid input: servo0 or servo1 must be integers.", 400
    
    if not response_messages:  # Tjekker om listen er tom
        return "No servo0 or servo1 provided", 400
    
    return "\n".join(response_messages), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8804)
