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
    sys.stderr.write("%s:1:1: error: ECU is not connected via USB.\r\n" % (sys.argv[0]))
    exit(1)
else:
    sys.stderr.write("%s:1:1: info: ECU is connected via USB. Using virtual port %s\r\n" % (sys.argv[0], port))
    sys.stderr.flush()

# Open connection
ser = serial.Serial(port, 9600)
if not ser.is_open:
    sys.stderr.write("%s:1:2: error: Could not open virtual port %s\r\n" % (sys.argv[0], port))
    exit(1)
else:
    sys.stderr.write("%s:1:2: info: Successfully opened port %s\r\n" % (sys.argv[0], port))
    sys.stderr.flush()

# Hard reset MCU
sys.stderr.write("%s:1:3: info: Starting test run by resetting ECU the hard way... " % (sys.argv[0]));
sys.stderr.flush()

ser.setDTR(True)
time.sleep(0.25);
ser.setDTR(False)

sys.stderr.write("Started\r\n");
sys.stderr.flush()

# Redirect byte stream from serial to stdout
sys.stderr.write("%s:1:4: info: Redirecting test-runner's output to stdout..." % (sys.argv[0]))
sys.stderr.flush()
# TODO: Implement this
sys.stderr.write(" Finished\r\n")
sys.stderr.flush()

# Close connection
ser.close()


# Thanks to:
# * http://stackoverflow.com/questions/2438848/set-serial-port-pin-high-using-python
# * http://www.hobbytronics.co.uk/arduino-tutorial9-power
# * https://www.embeddedrelated.com/showarticle/77.php
