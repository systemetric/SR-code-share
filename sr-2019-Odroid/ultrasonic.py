class Handler(object):
    """Handler class for ultrasonic sensors connected to the Ruggeduino

    NOTE - VARIABLES
    robot - instance of the sparklebot class
    numOf - Number of USSs connected to the ruggeduino

    NOTE - METHODS
    setup(numOf) - Called at init, tells the ruggeduino how many USSs are connected
    toggle() - Starts the ultrasonic sensors
    read() - Returns an array of integers that tell if the USSs can or can not see the ground
        - VALUES:
            0 - CANNOT see the ground
            1 - CAN see the ground
        - ORDER:
            The placement of the values in the array are based on the digital pins the USS is connected to.
            e.g. Index 0 is the USS connected to pin 3  
    """
    
    def __init__(self, robot, numOf=1):
        self.R = robot
        self.setup(numOf)

    def setup(self, numOf):
        for i in range(10):
            try:
                with self.R.ruggeduinos[0].lock:
                    self.R.ruggeduinos[0].command("u%s" % numOf)
            except Exception as e:
                print("Got %s when trying to setup US")
                print("Attempt %s" % i)
                time.sleep(0.1)
            
        
    def toggle(self):
        with self.R.ruggeduinos[0].lock:
            self.R.ruggeduinos[0].command("u1")
    
    def read(self):
        for i in range(10):
            try:
                value = self.R.RH.command("u2")
                if len(value) < 2:
                    continue
                print(value)
                returnValue = []
                for v in value.rstrip():
                    if v == '1':
                        returnValue.append(True)
                    else:
                        returnValue.append(False)
                print(returnValue)
                return returnValue
            except Exception as e:
                print(e)
