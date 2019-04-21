class Handler(object):
    """
    Handler of the gyro connected to the ruggeduino

    NOTE - VARIABLES
    PID - Dictionary of the PID values
        P - P value
        I - I value
        D - D value
    robot - Instance of the sparklebot class

    NOTE - METHODS
    readGyro() - Gets the average value of the gyro
    calcPID(error) - Calculates new PID values from the error
    start_reading() - Tell the ruggeduino to start reading the gyro
    stop_reading() - Tell the ruggeduino to stop reaing the gyro
    getValue() - Returns the value of the gyro from the ruggduino
    """
    def __init__(self, robot, PID):
        self.P = PID['P']
        self.I = PID['I']
        self.D = PID['D']

        self.R = robot
        # self.R.ruggeduinos[0].pin_mode(14, OUTPUT)

        self.lastError = 0
        self.i = 0
        self.baseVal = self.readGyro()
        if self.R.DEBUG:
            print("P: ", self.P)
            print("I: ", self.I)
            print("D: ", self.D)
            print("Base value: ", self.baseVal)

    def readGyro(self):
        sumVal = 0
        for x in range(0, 50):
            sumVal += self.getValue()
        if self.R.DEBUG: print("Voltage:", sumVal/1500)
        return sumVal/500

    def calcPID(self, error):
        p = abs(error)
        self.i += error
        d = abs(self.lastError) - abs(error)

        pidVal = self.P * p + self.I * self.i + self.D * d
        return pidVal

    def start_Reading(self):
        self.R.RH.command("x")

    def stop_Reading(self):
        self.R.RH.command("y")

    # Change command letter
    def getValue(self):
        for i in range(10):
            try:
                value = int(self.R.RH.command("z"))
                return (int(value)/1023.0) * 5.0
            except Exception as e:
                print(e)
                    
