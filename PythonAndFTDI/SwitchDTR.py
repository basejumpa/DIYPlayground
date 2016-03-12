import serial
import time
import sys
from subprocess import Popen, PIPE

# Read out assigned com port
port = ''
process = Popen(["reg", "query", "HKLM\\HARDWARE\\DEVICEMAP\\SERIALCOMM", "/v", "\\Device\\VCP0"], stdout=PIPE)
(output, err) = process.communicate()
exit_code = process.wait()
port = output.split()[3]

# Error handling
if port == '':
    sys.stderr.write("%s:1:1: error: ECU is not connected via USB." % (sys.argv[0]))
    exit(1)
else:
    sys.stderr.write("%s:1:1: info: ECU is connected via USB. Using virtual port %s" % (sys.argv[0], port))

# Open connection
ser = serial.Serial(port, 9600)

# Hard reset MCU
ser.setDTR(True)
time.sleep(0.25);
ser.setDTR(False)

# Redirect byte stream from serial to stdout
# TODO: Implement this

# Close connection
ser.close()


# Thanks to:
# * http://stackoverflow.com/questions/2438848/set-serial-port-pin-high-using-python
# * http://www.hobbytronics.co.uk/arduino-tutorial9-power
# * https://www.embeddedrelated.com/showarticle/77.php
