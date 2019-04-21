import sparklebot
import time

climbTime = 9
rPower = 17.553274682307162
lPower = 22.446725317692838

R = sparklebot.Robot()

try:
    startTime = time.time()

    R.releaseArms()
    R.releaseTail()
    print("Released stuff", time.time() - startTime)
    time.sleep(0.5)

    R.startEating()
    print("Started eating", time.time() - startTime)
    time.sleep(0.5)

    for n in range(5):
        print(R.motors[0].m0.power)
        # R.moveForTime(2)
        R.setMotors(lPower, rPower)
        time.sleep(2)
        R.setMotors(0, 0)
        print("Step %s of eating" % n, time.time() - startTime)
        time.sleep(3)

    R.moveForTime(15, power=-20)
    print("Reversed into first wall", time.time() - startTime)
    time.sleep(0.5)

    R.stopEating()
    print("Stopped eating", time.time() - startTime)
    time.sleep(0.5)


    distance = 0
    for i in range(10):
        markers = R.see()  # [m for m in R.see() if m.info.code == marker_code]

        for m in markers:
            if m.info.code == R.zone*7:
                distance = m.dist
        if distance < 5:
            R.moveForTime(4, power=45)
            print("Doing a step in moving 5m away from wall", time.time() - startTime)
            time.sleep(1)
        else:
            break
    print("Reached the distance of 5m away from wall", time.time() - startTime)
    time.sleep(0.5)

    distance = 4.1
    for i in range(15):
        markers = R.see()  # [m for m in R.see() if m.info.code == marker_code]
        for m in markers:
            if m.info.code == R.zone*7:
                distance = m.dist
        if distance > 4:
            R.moveForTime(5, power=-20)
            print("Doing a step in moving back to 4m away from wall",
                time.time() - startTime)
            time.sleep(1)
        else:
            break

    R.turn90()
    print("Turned 90 to face caldera", time.time() - startTime)
    time.sleep(0.5)

    R.moveForTime(10, power=-20)
    print("Reversed into second wall", time.time() - startTime)
    time.sleep(0.5)

    # rot = 0
    # for i in range(20):
    #     makrers = R.see()
    #     for m in markers:
    #         if m.info.code == 3 + R.zone*7:
    #             rot = m.rot_y
    #     if rot < -5:
    #         R.turnForTime(1, -1)
    #     elif rot > 5:
    #         R.turnForTime(1, 1)
    #     else:
    #         break

    R.moveForTime(climbTime, power=70)
    print("Climbed the arena", time.time() - startTime)
    time.sleep(0.5)

    R.moveUntilStep(timeout=10)
    print("Reached the edge or it took to long", time.time() - startTime)
    time.sleep(0.5)

    print("Will now vomit cubes", time.time() - startTime)
    R.vomit()
    while time.time() - startTime < 145:
        R.turnForTime(0.25, 1, power=50)
        R.turnForTime(0.25, -1, power=50)

    R.stopEating()
    R.setMotors(0, 0)
    print("Finishd yayyyyyyyyyyyyy", time.time() - startTime)
    time.sleep(0.5)
except Exception as e:
    print("Got %s as overall" % e)
    print("Using backup")

    R.releaseArms()
    R.releaseTail()

    R.setMotors(30, 33)
    time.sleep(15)
    R.setMotors(0, 0)
