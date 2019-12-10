import kinematics
import time
from math import pi
from math import *
import RPi.GPIO as GPIO

servoPIN_1 = 4
servoPIN_2 = 17
servoPIN_3 = 22
servoPIN_4 = 10

class meArm():
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		self.plist = [servoPIN_1, servoPIN_2, servoPIN_3, servoPIN_4]
		for pin in self.plist:
			GPIO.setup(pin, GPIO.OUT)

		p1 = GPIO.PWM(servoPIN_1, 50)
		p2 = GPIO.PWM(servoPIN_2, 50)
		p3 = GPIO.PWM(servoPIN_3, 50)
		p4 = GPIO.PWM(servoPIN_4, 50)

		self.servoPWM = {}
		self.servoPWM["base"] = p1
		self.servoPWM["shoulder"] = p2
		self.servoPWM["elbow"] = p3
		self.servoPWM["gripper"] = p4

		print("Init Servo")
		for p in self.servoPWM.values():
			p.start(7.5)
			time.sleep(0.5)
		print("Fin init")

		self.baseAngle = 0
		self.shoulderAngle = 0
		self.elbowAngle = 0

	def rad2deg(self, angle):
		return (angle / pi) * 180.0

	def deg2rad(self, angle):
		return pi * angle / 180.0

	def rotateDegreeBasic(self, pName, degree):
		cycleLen = 7.5 + (degree / 90.0) * 5
		#if cycleLen > 12.5 or
		if cycleLen < 2.5:
			return False
		self.servoPWM[pName].ChangeDutyCycle(cycleLen)
		return True

	def rotateDegree(self, pName, degree, lastDegree):
		cycleLen = 7.5 + (degree / 90.0) * 5
		#if cycleLen > 12.5 
		if cycleLen < 2.5:
			return False
		if int(lastDegree) ==  int(degree):
			return True
		if int(lastDegree) < int(degree):
			step = -5
		if int(lastDegree) > int(degree):
			step = 5
		for deg in range(int(degree), int(lastDegree), step):
			cycleLen = 7.5 + (deg / 90.0) * 5
			self.servoPWM[pName].ChangeDutyCycle(cycleLen)
		time.sleep(0.2)	
		return True
			
	def gotoPoint(self, x, y, z):
		if y == 0:
			y = 1
		tempBaseAngle = self.rad2deg(atan(y/x))
		distance = sqrt(pow(x, 2) + pow(y, 2))

		
		print(distance, (distance - 90) / 90)
		shoulderGrad = asin((distance - 90)/ 90)
		
		tempShoulderAngle = self.rad2deg(shoulderGrad)
		baseHeight = 90 * cos(shoulderGrad) + 60

		elbowGrad = asin((z - baseHeight) / 90)
		print((z - baseHeight) / 90)
		tempElbowAngle = self.rad2deg(elbowGrad)

		print("Angles: {}, {}, {}".format(tempBaseAngle, tempElbowAngle, tempShoulderAngle))
		if self.rotateDegreeBasic("base", tempBaseAngle):
			self.baseAngle = tempBaseAngle
		
		if self.rotateDegreeBasic("shoulder", tempShoulderAngle):
			self.shoulderAngle = tempShoulderAngle

		if self.rotateDegreeBasic("elbow", tempElbowAngle):
			self.elbowAngle = tempElbowAngle

	def resetAll(self):
		print("Resetting Servo")
		for p in self.servoPWM.values():
			p.start(7.5)
			time.sleep(0.5)
		print("Fin reset")

		self.baseAngle = 0
		self.shoulderAngle = 0
		self.elbowAngle = 0

	def goBack(self):
		angle = self.baseAngle
		rad = 76
		self.gotoPoint(rad * cos(self.deg2rad(angle)), rad * sin(self.deg2rad(angle)), 70)
		

	def moveForward(self):
		angle = self.baseAngle
		rad = 178
		self.gotoPoint(rad * cos(self.deg2rad(angle)), rad * sin(self.deg2rad(angle)), 70)
		

	def goPick(self):
		self.openGripper()
		self.moveForward()
		time.sleep(2)
		self.closeGripper()
		self.goBack()

	def goRelease(self):
		self.moveForward()
		self.openGripper()
		time.sleep(2)
		self.goBack()
		self.closeGripper()

	def turnBase(self, angle):
		self.rotateDegreeBasic("base", angle)
		self.baseAngle = angle

		
	def openGripper(self):
		"""Open the gripper, dropping whatever is being carried"""
		self.rotateDegreeBasic("gripper", 20)
		time.sleep(0.3)
		
	def closeGripper(self):
		"""Close the gripper, grabbing onto anything that might be there"""
		self.rotateDegreeBasic("gripper", 100)
		time.sleep(0.3)

	def getPos(self):
		"""Returns the current position of the gripper"""
		return [self.baseAngle, self.outreach, self.heightAdj]
