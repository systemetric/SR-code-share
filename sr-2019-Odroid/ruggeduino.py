class Handler(object):
    """
    Handler class for talking to Ruggeduinos

    NOTE - VARIABLES
    robot - Instance of the sparklebot class
    num - Index of the ruggeduino in ruggeduinos[]
    
    NOTE - METHODS
    command(cmd) - Send a string (cmd) to the ruggedunio, returns the response.
    """

    def __init__(self, robot, num=0):
        self.R = robot
        self.num = num

    def command(self, cmd):
        with self.R.ruggeduinos[self.num].lock:
            res = self.R.ruggeduinos[self.num].command(cmd)
        return res
