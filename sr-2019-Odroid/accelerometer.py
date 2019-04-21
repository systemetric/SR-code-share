class Handler(object):
    def __init__(self, robot):
        self.R = robot

        self.baseVal = [0,0,0]
        for i in range(10):
            value = self.getValue()
            print(value)
            for v in range(3):
                self.baseVal[v] += value[v]
        for v in range(3):
            self.baseVal[v] /= 10
            self.baseVal[v] = round(self.baseVal[v], 1)

    def getValue(self):
        for i in range(10):
            try:
                values = self.R.RH.command("a")
                if values != '':
                    break
            except Exception as e:
                print(e)
        return [round(float(value), 1) for value in values.split(',')]
