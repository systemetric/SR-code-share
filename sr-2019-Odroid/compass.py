class Handler(object):
    """
    Handler for the compass connected to the ruggeduino

    NOTE - VARIABLES
    PID - Dictionary of PID values
        P - P value
        I - I value
        D - D value
    robot - Instance of sparklebot class

    NOTE - METHODS
    calcPID(error) - Calculate the new PID values from the given error
    getValue() - Gets the heading from the compass
    """
    def __init__(self, robot, PID): 
        self.P = PID['P']
        self.I = PID['I']
        self.D = PID['D']

        self.R = robot

        self.lastError = 0
        self.i = 0
        if self.R.DEBUG:
            print("P: ", self.P)
            print("I: ", self.I)
            print("D: ", self.D)

    def calcPID(self, error):
        "Calculate the new PID values from error"
        p = abs(error)
        self.i += error
        d = abs(self.lastError) - abs(error)
        pidVal = self.P * p + self.I * self.i + self.D * d
        return pidVal


    def getValue(self):
        "Gets the heading from the compass"
        heading = self.R.RH.command("e")
        value = int(float(heading))
        return(value)
