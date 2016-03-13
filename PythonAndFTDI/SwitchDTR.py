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
    sys.stderr.write("%s:1:1: error: ECU is not connected via USB.\r\n" % __file__)
    exit(1)
else:
    sys.stderr.write("%s:1:1: info: ECU is connected via USB. Using virtual port %s\r\n" % (__file__, port))
    sys.stderr.flush()

# Open connection
ser = serial.Serial(port, 9600, timeout=5)
if not ser.is_open:
    sys.stderr.write("%s:1:2: error: Could not open virtual port %s\r\n" % (__file__, port))
    exit(1)
else:
    sys.stderr.write("%s:1:2: info: Successfully opened port %s\r\n" % (__file__, port))
    sys.stderr.flush()

# Hard reset MCU
sys.stderr.write("%s:1:3: info: Starting test run by resetting ECU the hard way... " % __file__);
sys.stderr.flush()

ser.setDTR(True)
time.sleep(0.25);
ser.setDTR(False)

sys.stderr.write("Started\r\n");
sys.stderr.flush()

# Redirect byte stream from serial to stdout
sys.stderr.write("%s:1:4: info: Redirecting test-runner's output to stdout..." % __file__)
sys.stderr.flush()
while True:
    c = ser.read()
    if len(c) == 0:
        sys.stderr.write(" TIMEOUT\r\n%s:1:5: error: Timeout occurred. Didn't receive any character for more than %i seconds.\r\n" % (__file__, ser.timeout))
        ser.close()
        exit(1)
    elif c == 'Z':
        ser.close()
        sys.stderr.write(" Finished\r\n")
        sys.stderr.flush()
        break
exit(0)

# Thanks to:
# * http://stackoverflow.com/questions/2438848/set-serial-port-pin-high-using-python
# * http://www.hobbytronics.co.uk/arduino-tutorial9-power
# * https://www.embeddedrelated.com/showarticle/77.php
