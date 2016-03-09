from arduino import Arduino
import time

b = Arduino('COM4')
pin = 5

#declare output pins as a list/tuple
b.output([pin])

for i in range(10):
    b.setHigh(pin)
    print b.getState(pin)
    time.sleep(1)
    b.setLow(pin)
    print b.getState(pin)
    time.sleep(1)
b.close()

