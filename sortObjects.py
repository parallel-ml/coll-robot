from __future__ import print_function
import pycreate2
import time
import math
from myMovement import meArm
from easydetect import detect
    

if __name__ == "__main__":
    arm = meArm()
    port = '/dev/ttyUSB0'  # this is the serial port on my raspberry pi
    baud = {
		'default': 115200,
		'alt': 19200  # shouldn't need this unless you accidentally set it to this
	}

    bot = pycreate2.Create2(port=port, baud=baud['default'])
    #can pick locations arbitrarily        
    location1 = [50,50]
    location2 = [-50, -50]
    location3 = [50, 100]
    
    currentLocation = [0,0]
    currentAngle = 0

    #assumes no obstacle
    #if obstacle, moveTo intermittent locations to go around obstace
    def moveTo(current, heading, destination):
        distance = (destination[0] - current[0]) ** 2
        distance += (destination[1] - current[1]) ** 2
        distance **= 1/2
        angle = math.atan2(destination[1] - current[1],
                            destination[0] - current[0])
        #turn = math.degrees(abs(heading - angle))
        turn = math.degrees(angle - heading)
        bot.turn_angle(turn)

        #  if turn > 180:
        #       bot.turn_angle(-1 * turn)
        currentAngle = angle
        bot.drive_distance(distance, stop=True)
        currentLocation = destination
        
    bot.start()
    bot.safe()
    moveTo(currentLocation, currentAngle, location1)
#check item is within range with size w/ cv maybe
#do checking and pickup item with arm code
#arm.closeGripper()

    def simplemove():
        bot.drive_distance(100)

    arm.turnBase(-25)
    arm.goPick()

    result = detect()
    print("Yellow mark found?: {}".format(result))

    moveTo(currentLocation, currentAngle, location2)
    arm.goRelease()
    
#moveTo(currentLocation, currentAngle, location2)
#arm.openGripper()
#repeat this for all locations
            
    print('stopping')
    bot.drive_stop()
    time.sleep(0.1)
