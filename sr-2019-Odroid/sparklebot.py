# SR stuff
import sr.robot
import time
import serial
import sys

# Math functions
from math import sin, cos, radians

# Constants
from sr.robot import (MARKER_ARENA, MARKER_TOKEN, OUTPUT, INPUT, INPUT_PULLUP)

# Handlers
import ruggeduino
import ultrasonic
import compass
import gyro
import accelerometer


def sign(x):
    return -1 if x < 0 else (1 if x > 0 else 0)


class Robot(sr.robot.Robot):

    # TODO: define below
    MULTIPLIER_LEFT = 1
    MULTIPLIER_RIGHT = 1
    STARTUP_TIME = 0.25
    eatingPower = 80
    timeFor90 = 3.075#2.71#3.51 32.48
    powerToSpeed = {
        20: 0.1121,
        50: 0.5298,
        -50: 0.5
    }

    # NOTE - Variable things to check in final arena
    # - PID values
    # - SPEED of robot at certain power values
    # - index of which camera is which

    def __init__(self, gyroPID={'P': 300, 'I': 0, 'D': 295}, DEBUG=False):

        self.ruggeduinoCheck()

        super(Robot, self).__init__()
        self.DEBUG = DEBUG
        self.RH = ruggeduino.Handler(self)  # Handler for ruggeduino
        self.USH = ultrasonic.Handler(self, numOf=2)  # Handler for ultasonic sensor
        self.GH = gyro.Handler(self, gyroPID)  # Handler for gyro
        # self.CH = compass.Handler(self, compassPID)  # Handler for compass
        # self.AH = accelerometer.Handler(self)  # Handler for accelerometer
        self.gyroPID = gyroPID
        # self.compassPID = compassPID

    def ruggeduinoCheck(self):
        for n, dev in enumerate(self._list_usb_devices("Ruggeduino", subsystem="tty")):
            self.serial = serial.Serial(dev.device_node, 115200, timeout=0.1)
            for i in range(10):
                self.serial.write("v")
                res = self.serial.readline()
                if len(res) > 0 and res[-1] == "\n":
                    break
            if i == 9:
                sys.exit()

    def status(self):
        print("----------STATUS----------")
        print("Battery Voltage - ", self.power.battery.voltage)
        print("DEBUG - %s" % self.DEBUG)
        print("PID values: ")
        print("     Gyro - %s" % self.gyroPID)
        print("     Compass - %s" % self.compassPID)
        print("Handlers: ")
        print("     Ruggeduino - %s" % hasattr(self, 'RH'))
        print("     Ultrasonic - %s" % hasattr(self, 'USH'))
        print("     Gyro - %s" % hasattr(self, 'GH'))
        print("     Compass - %s" % hasattr(self, 'CH'))
#---------------------------------------
#       MOVEMENT - NOTE

    def setMotors(self, left, right):
        self.motors[1].m1.power = -left
        self.motors[0].m1.power = -right
        # if self.DEBUG:
        #     print("Set left and right motor powers to: %s, %s" % (left, right))

    def move(self, distance, power=50):
        move_time = abs(distance) / self.powerToSpeed[sign(distance)*power]
        lPower = sign(distance) * power
        rPower = sign(distance) * power
        self.setMotors(lPower, rPower)
        start_time = time.time()
        while time.time() - start_time < move_time:
            error = self.GH.getValue()/10 - self.GH.baseVal
            if error != 0:
                pidVal = self.GH.calcPID(error)

                if error > 0:
                    lPower -= pidVal
                    rPower += pidVal
                else:
                    lPower += pidVal
                    rPower -= pidVal

                rPower = max(min(100, rPower), -100)
                lPower = max(min(100, lPower), -100)
                self.setMotors(lPower, rPower)

            else:
                self.GH.i = 0

            if self.DEBUG:
                print("Error: ", error)
                print(" PID Value: ", pidVal)
                print("Voltage: ", self.GH.getValue())
                print("Left Power: ", lPower)
                print("Right Power: ", rPower)

        self.setMotors(0, 0)
        if self.DEBUG:
            print("Moved a distance of %s in a time of %s" %
                  distance, move_time)

    # ATTENTION DO NOT USE YET

    def turnForTime(self, t, m, power=20):
        self.setMotors(power*m, -power*m)
        time.sleep(t)
        self.setMotors(0,0)

    def turnWithCompass(self, angle, power=20):
        currAngle = self.CH.getValue()
        targetAngle = currAngle + angle
        lPower = 0
        rPower = 0

        print(currAngle, targetAngle)

        self.setMotors(lPower, rPower)
        lastAngle = self.CH.getValue()
        while currAngle != targetAngle:
            try:
                currAngle = self.CH.getValue()
                while currAngle == 0:
                    self.CH.getValue()
                if lastAngle - currAngle > 180:
                    targetAngle = targetAngle % 360
                elif lastAngle - currAngle < -180:
                    targetAngle += 360

                error = targetAngle - currAngle
                if error != 0:
                    pidVal = self.CH.calcPID(error)

                    if error > 0:
                        lPower = power+pidVal
                        rPower = -power-pidVal
                    else:
                        lPower = -power-pidVal
                        rPower = power+pidVal

                    rPower = max(min(50, rPower), -50)
                    lPower = max(min(50, lPower), -50)
                    self.setMotors(lPower, rPower)
                    lastAngle = currAngle
                    if self.DEBUG:
                        print("Error: ", error, "| PID Value: ", pidVal, "| Target Angle: ", targetAngle,
                              "| Heading: ", currAngle, "| Left Power: ", lPower, "| Right Power: ", rPower)

                else:
                    self.CH.i = 0

                if abs(error) < 2:
                    self.setMotors(0, 0)
                    break
            except:
                pass
        self.setMotors(0, 0)
        if self.DEBUG:
            print("Turned an angle of %s" % angle)

    def turn90(self):
        self.turnForTime(self.timeFor90, -1)    

    def moveUntil(self, condition, power=20):
        "Moves unil condition, a function, is false"
        lPower = power
        rPower = power
        while condition():
            error = self.GH.getValue()/10 - self.GH.baseVal
            if error != 0:
                pidVal = self.GH.calcPID(error)

                if error > 0:
                    lPower -= pidVal
                    rPower += pidVal
                else:
                    lPower += pidVal
                    rPower -= pidVal

                rPower = max(min(100, rPower), -100)
                lPower = max(min(100, lPower), -100)
                self.setMotors(lPower, rPower)
            else:
                self.GH.i = 0

        self.setMotors(0, 0)

    def moveForTime(self, t, power=20):
        lPower = power
        rPower = power
        if self.DEBUG:
            print("Moving for a time of %ss at a power of %s" % (t, power))
        startTime = time.time()
        self.setMotors(lPower, rPower)
        while time.time() - startTime < t:
            error = self.GH.getValue()/10 - self.GH.baseVal
            # print("Value: ", self.AH.getValue())
            if error != 0:
                pidVal = self.GH.calcPID(error)

                if error > 0:
                    lPower -= pidVal
                    rPower += pidVal
                else:
                    lPower += pidVal
                    rPower -= pidVal

                rPower = max(min(100, rPower), -100)
                lPower = max(min(100, lPower), -100)
                print(lPower, rPower)
                self.setMotors(lPower, rPower)
            else:
                self.GH.i = 0
        self.setMotors(0, 0)
        if self.DEBUG: print("Stopped")

    def climb(self, power=50):
        lPower = power
        rPower = power

        isClimbing = False
        isOnTop = False

        self.setMotors(lPower, rPower)
        while isClimbing is False or isOnTop is False:
            currentValue = self.AH.getValue()
            if isClimbing is False:
                if currentValue != self.AH.baseVal:
                    isClimbing = True
                    print("Now climbing")
                    self.beep('c')
                else:
                    print("Not at step yet")
            else:
                if isOnTop is False:
                    if currentValue == self.AH.baseVal:
                        isOnTop = True
                        print("Now on top")
                    else:
                        print("Still climbing")
                else:
                    print("This shouldn't be possible")

            error = self.GH.getValue()/10 - self.GH.baseVal
            if error != 0:
                pidVal = self.GH.calcPID(error)

                if error > 0:
                    lPower -= pidVal
                    rPower += pidVal
                else:
                    lPower += pidVal
                    rPower -= pidVal

                rPower = max(min(100, rPower), -100)
                lPower = max(min(100, lPower), -100)
                self.setMotors(lPower, rPower)

            else:
                self.GH.i = 0

            if self.DEBUG:
                print("Error: ", error)
                print("PID Value: ", pidVal)
                print("Voltage: ", self.GH.getValue())
                print("Left Power: ", lPower)
                print("Right Power: ", rPower)
                print("Base value of accelerometer: ", self.AH.baseVal)
                print("Current value of accelerometer: ", currentValue)
                print("isClimbing: ", isClimbing)
                print("isOnTop: ", isOnTop)
        self.setMotors(0,0)

    def moveUntilStep(self, power=20, timeout=100000):
        lPower = power
        rPower = power
        self.USH.toggle()
        while any(self.USH.read()) and time.time() + timeout >= time.time():
            print(self.USH.read())
            error = self.GH.getValue()/10 - self.GH.baseVal
            if error != 0:
                pidVal = self.GH.calcPID(error)

                if error > 0:
                    lPower -= pidVal
                    rPower += pidVal
                else:
                    lPower += pidVal
                    rPower -= pidVal

                rPower = max(min(100, rPower), -100)
                lPower = max(min(100, lPower), -100)
                self.setMotors(lPower, rPower)
            else:
                self.GH.i = 0
        self.setMotors(0, 0)
        self.USH.toggle()
#---------------------------------------
#       VISION AND MOVEMENT - NOTE
    def scanForMarkers(self, marker_type, corner=-1):
        """
        Returns a list of markers of the type `marker_type`
        """
        if marker_type is MARKER_TOKEN:
            if (corner < 0) or (corner > 4):
                raise ValueError("Invalid corner number")
            else:
                acceptable_types = [MARKER_TOKEN, corner]
            print("Looking a token of team %s..." % corner)

        elif marker_type is MARKER_ARENA:
            acceptable_types = [MARKER_ARENA] + range(28)
            print("Looking for wall markers...")
        else:
            raise ValueError("Invalid marker_type")

        while True:
            markers = self.see()
            acceptable_markers = [m for m in markers if (
                m.info.marker_type in acceptable_types)]
            # and (m.info.offset in acceptable_types)

            if acceptable_markers:
                return acceptable_markers

            print("No acceptable markers found, turning  to try again")
            self.turn(45)
            time.sleep(0.3)

    def scanForMarker(self, marker_code):
        """
        Returns a marker with the .info.code == `marker_code`
        """
        print("Finding marker %s" % marker_code)
        while True:
            # marker = self.see(filter=lambda res:[ m for m in res if m.info.code == marker_code ])
            marker = [m for m in self.see() if m.info.code == marker_code]

            if marker:
                return marker

            print("Marker %s not found, turning  to try again" % marker_code)
            self.turn(20)
            time.sleep(0.3)

    def lineUpOnMarker(self, marker):
        direction = sign(marker.rot_y)

        angle = 180 - (direction*marker.rot_y + 90) - \
            direction*marker.orientation.rot_y

        distance = sin(abs(marker.rot_y)) * self.getFloorDistance(marker)

        self.goToRelativePos(angle, distance)
        self.turn(dir * 90)

    def getFloorDistance(self, marker):
        # zDist = sin(90 + radians(marker.centre.polar.rot_x)) * marker.dist
        # return(zDist / (cos(radians(marker.centre.polar.rot_y))))
        # OR
        return marker.dist * cos(radians(marker.centre.polar.rot_x))
        # OR
        # return marker.centre.world.z
#----------------------------------------
#       BODY PARTS - NOTE

    def startEating(self):
        self.motors[0].m0.power = self.eatingPower
        if self.DEBUG: print("Started eating")

    def stopEating(self):
        self.motors[0].m0.power = self.motors[0].m0.power*0.5
        time.sleep(0.5)
        self.motors[0].m0.power = self.motors[0].m0.power*0.25
        time.sleep(0.5)
        self.motors[0].m0.power = self.motors[0].m0.power*0.1
        time.sleep(0.5)
        self.motors[0].m0.power = 0
        if self.DEBUG: print("Stopped threshers")

    def vomit(self):
        self.motors[0].m0.power = -self.eatingPower
        if self.DEBUG: print("Started vomiting")

    def releaseTail(self):
        self.servos[0][0] = 150
        self.servos[0][1] = -150
        if self.DEBUG:  print("Tail released")
    
    def releaseArms(self):
        self.servos[0][2] = -100
        self.servos[0][3] = 100

    def beep(self, n):
        self.power.beep(500, note=n)
#----------------------------------------
