import serial
import time

ser = serial.Serial('COM6', 9600)
while True:
	ser.setDTR(False);
	time.sleep(1)
	ser.setDTR(True);
	time.sleep(1)

# Thanks to:
# * http://stackoverflow.com/questions/2438848/set-serial-port-pin-high-using-python
# * http://www.hobbytronics.co.uk/arduino-tutorial9-power
# * https://www.embeddedrelated.com/showarticle/77.php