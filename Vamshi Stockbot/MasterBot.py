import time
from datetime import datetime
import urllib3
import twilio.twiml
from twilio.rest import Client
from bot import bot

global extraBots
extraBots = 0

global numBots
numBots = 0

def updateNumBots(newNum):
	global numBots
	# bots = open('./.txt').readline().strip()
	poop = '{}Memory/numbots.txt'.format(bot.getRootPath())
	# print(poop)
	file = open('{}Memory/numbots.txt'.format(bot.getRootPath()), 'w')
	numBots = newNum
	file.write(str(newNum))	
	file.close()

def sendMessage(message):
	account_sid = "AC1b5e12de87f77753a3f18e20da8f2da7"
	auth_token = "321da7ec3fb12c2083e11c3f935f8109"
	client = Client(account_sid, auth_token)
	client.api.account.messages.create(to="+18179078815", from_="+18175838410", body=message)

def monitor():
	global numBots
	global extraBots

	targetDir = './Assignments/'

	Assignments = os.listdir(targetDir)
	newAssignment = open(targetDir+bot.PCID()).readline().strip()
	if newAssignment == '': newAssignment = None

	if newAssignment != None:
		time.sleep(180)
		if newAssignment == open(targetDir+bot.PCID()).readline().strip():
			out = open(targetDir+newAssignment, 'w')
			out.write("terminate")
			extraBots +=1



	

def initiatePredictors():
	http = urllib3.PoolManager()
	updateNumBots('5')
	http.request('POST', 'localhost:5000/task/predictors')


def initiateCheck():
	http = urllib3.PoolManager()
	updateNumBots('1')
	http.request('POST', 'localhost:5000/task/check')
	
# def initiate



def main():
	# ##Timed reminder
	# x =datetime.now()
	# y = datetime(x.year, x.month, x.day, 23, 59, 0)

	# while 2>1:
	# 	x =datetime.now()

	# 	if x>y:
	# 		print(True)
	# 		time.sleep(5)
	# 		initiatePredictors()
	# 		x =datetime.now()
	# 		y = datetime(x.year, x.month, x.day, 23, 59, 0)
	# 	else:
	# 		print(False)
	# 		time.sleep(200)



	# http = urllib3.PoolManager()
	# http.request('POST', 'localhost:5000/task/check')
	# sendMessage("Checking accuracy of predictions")

	initiatePredictors()

	# while 2>1:
	# 	x =datetime.now()
	# 	y = datetime(2017, 8, 10, 0, 0, 0)

	# 	if x>y:
	# 		print(True)
	# 		http = urllib3.PoolManager()
	# 		http.request('POST', 'localhost:5000/task/predictors')
	# 		# sendMessage("Checking accuracy of predictions")
	# 		break

	# 	else:
	# 		print(False)
	# 		time.sleep(200)
	ooppoo = 3
main()
