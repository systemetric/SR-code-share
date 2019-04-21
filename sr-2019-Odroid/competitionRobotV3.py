import sparklebot
import time

R = sparklebot.Robot()

startTime = time.time()

R.releaseArms()
R.releaseTail()

R.setMotors(50, 56)
time.sleep(7)
R.setMotors(0,0)

R.setMotors(-20, -20)
time.sleep(3)
R.setMotors(0, 0)

# for i in range(3):
#     R.turnForTime(1, 1)
#     R.turnForTime(1, -1)

R.setMotors(95, 95)
time.sleep(5)
R.setMotors(0,0)


R.setMotors(-20, -20)
time.sleep(1.5)
R.setMotors(0, 0)

# for i in range(3):
#     R.turnForTime(1, 1, power=40)
#     R.turnForTime(1, -1, power=40)
    

while time.time() - startTime < 145:
    scale = ["a", "b", "c", "d", "e", "f", "g"]
    song = [2, 2, 3, 4, 3, 2, 6, 4, 2, 6]
    for note in song:
        R.beep(scale[note])
