"""
run this on start-up by entering into terminal:
sudo nano /etc/rc.local
and add:
python3 /home/pi/Camera/main.py &
exit 0
currently supported signs:
TESTMSG, TAKEPIC, DEEPLOY, SUICIDE
"""
import argparse
import digitalio
import board
from nrf_com.nrf_communicate import NRF_communicate, Sign
import time
from picamera import PiCamera
from camsign import CamSign

parser = argparse.ArgumentParser()
parser.add_argument("--testmode", help="set to run test mode",
                    action="store_true")
args = parser.parse_args()

def test_msg(led):
    print("testing, TESTING, 1, 2, 3...")
    led.value = True
    time.sleep(1)
    led.value = False
#this flips the magnet state, thus working for DEEPLOY and SUICIDE
def flip_mag(mag):
    mag.value = True
    time.sleep(.2)
    mag.value = False

ce = digitalio.DigitalInOut(board.CE0)
csn = digitalio.DigitalInOut(board.D25)
led = digitalio.DigitalInOut(board.D14)
led.direction = digitalio.Direction.OUTPUT
mag = digitalio.DigitalInOut(board.D15)
mag.direction = digitalio.Direction.OUTPUT

address = [b"CAMRA", b"RIVER"]

test_sign = Sign("TESTMSG", act_on_sign=True, funct=test_msg, args=[led])
deploy_sign = Sign("DEEPLOY", act_on_sign=True, funct=flip_mag, args=[mag])
sui_sign = Sign("SUICIDE", act_on_sign=True, funct=flip_mag, args=[mag])
class CamSign(Sign):
    def __init__(self):
        from picamera import PiCamera
        self.count = 0
        self.name = "TAKEPIC"
        self.camera = PiCamera()
        self.camera.resolution = ((3280, 2464),
                                  (1024, 768),
                                  (640, 480))[0]
        self.camera.rotation = (0, 90, 180, 270)[2]
        
    def on_sign(self, semisig = '---'):
        stream=open("./pics/img{}.png".format(self.count), 'wb')
        self.camera.capture(stream, format='jpeg')
        stream.close()
        self.count += 1
        
cam_sign = CamSign()

test_mode = args.testmode
while(test_mode):
    test_sign.on_sign()
    time.sleep(2)
    cam_sign.on_sign()
    time.sleep(8)
    print("test sequence repeat loop")

nrf_com = NRF_communicate(ce, csn, address[0], address[1], \
                signs=(test_sign, cam_sign, deploy_sign, sui_sign), 
                encode = False)
print("waiting for sign...")
while(True):
    sign = nrf_com.block_until_sign()
    if(sign == "TAKEPIC"):
        
    print("sign found")