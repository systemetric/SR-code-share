import sparklebot, time
climbTime=6

R = sparklebot.Robot()
FinishTime = time.time() + 150

R.status()

R.releaseArms()
R.releaseTail()
print("Arms relaesed ", FinishTime - time.time())
time.sleep(0.5)

R.startEating()
print("Started Eating ", FinishTime - time.time())
time.sleep(0.5)

for n in range(5):
    R.move(0.34, power=20)
    print("Step %s" % n, FinishTime - time.time())
    time.sleep(3)

R.stopEating()
print("Stopped eating", FinishTime - time.time())
time.sleep(0.5)

R.move(-1)
print("Moved back", FinishTime - time.time())
time.sleep(0.5)

R.turnForTime(1.6, -1)
print("Turned for 1.6s anticlockwise ", FinishTime - time.time())
time.sleep(0.5)

R.move(1.5)
print("Moved forward ", FinishTime - time.time())
time.sleep(0.5)

R.turnForTime(1.6, 1)
print("Turned for 1.6s clockwise ", FinishTime - time.time())
time.sleep(0.5)

R.move(1)
print("Moved Forward", FinishTime - time.time())
time.sleep(0.5)

R.turnForTime(3.075, -1)
print("Turned 90 anticlockwise", FinishTime - time.time())
time.sleep(0.5)

# R.turn90()
# time.sleep(0.5)
# R.turn90()
# print("Turned 180 ", FinishTime - time.time())
# time.sleep(0.5)

# R.move(1.2)
# print("Moved to step", FinishTime - time.time())
# time.sleep(0.5)

R.moveForTime(climbTime, power=65)
print("Climbed step", FinishTime - time.time())
time.sleep(0.5)

# R.climb()
# time.sleep(0.5)

# R.moveUntilStep(timeout=FinishTime - time.time() - 30)
R.moveUntilStep()
print("Reached caldera", FinishTime - time.time())
time.sleep(0.5)

R.vomit()
print("Will now vomit cubes", FinishTime - time.time())
while FinishTime - time.time() > 5:
    R.turnForTime(0.25, 1, power=50)
    R.turnForTime(0.25, -1, power=50)
R.stopEating()
R.setMotors(0,0)
