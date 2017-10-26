from flask import Flask, request, redirect, render_template
import os
import urllib3
from bs4 import BeautifulSoup 
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import certifi
import re
import math
from datetime import date, timedelta,datetime
import os
import winreg
import random
import urllib
import pyautogui
from bot import bot
import twilio.twiml
from twilio.rest import Client

global tasks
global progress
global bots 
global botQueue
bots = {}
botQueue = 0
tasks = []
progress = []

def sendMessage(message):
	account_sid = "AC1b5e12de87f77753a3f18e20da8f2da7"
	auth_token = "321da7ec3fb12c2083e11c3f935f8109"
	client = Client(account_sid, auth_token)
	client.api.account.messages.create(to="+18179078815", from_="+18175838410", body=message)

def updateNumBots(newNum):
	# bots = open('./.txt').readline().strip()
	poop = '{}Memory/numbots.txt'.format(bot.getRootPath())
	# print(poop)
	file = open('{}Memory/numbots.txt'.format(bot.getRootPath()), 'w')
	file.write(str(newNum))	
	file.close()


# @app.route('/authorize/<poop>')
# def authorize(poop):
# 	number = ""
def generateBotID():
	global bots
	duplicate = True
	botID = 0
	while duplicate:
		duplicate = False
		botID = random.randrange(1,200000)
		if botID in bots:
			duplicate = True
			continue
	return str(botID)

def getTask():
	global tasks
	if len(tasks) == 0:
		return "terminate"
	else:
		for task in tasks:
			if task in progress:
				continue
			else:
				progress.append(task)
				return task
		return "terminate"

def spawnBot():
	botID = generateBotID()

	file = open('./Assignments/{}.txt'.format(bot.PCID()), 'w')
	file.write(botID)
	file.close()

	assignBot(botID)

	pyautogui.hotkey('win', 'r')
	pyautogui.typewrite("cmd", interval=0.25)
	pyautogui.hotkey('enter')
	time.sleep(.5)
	pyautogui.typewrite("cd onedrive/bots/stockbot")
	pyautogui.hotkey('enter')
	if bot.PCID() == "Vamshi":
		pyautogui.typewrite("WorkerBot.py")
	else:
		pyautogui.typewrite("py WorkerBot.py")
	pyautogui.hotkey('enter')

def assignBot(botID):
	task = getTask()

	file = open('./Assignments/{}.txt'.format(botID), 'w')
	file.write(task)
	file.close()

def initiateCheck():
	global botQueue
	global tasks

	botQueue = 1

	tasks.append('check')

	checkBotQueue()

def initiatePredictors():
	global botQueue
	global tasks
	
	botQueue = 5
	data = open('./targets.txt')
	for line in data:
		term = line.strip()
		tasks.append('predict:{}'.format(term))
	checkBotQueue()

def checkBotQueue():
	global botQueue
	if botQueue >0:
		spawnBot()

def clearAssignment():
	open('./Assignments/'+bot.PCID(), 'w')

#route urls
app = Flask(__name__)

@app.route('/alive/<botID>', methods=['POST'])
def alive(botID):
	global botQueue
	bots[botID] = "alive"
	botQueue -=1

	clearAssignment()
	
	checkBotQueue()
	return "poop"


@app.route('/task/<task>', methods=['POST'])
def task(task):
	print("here")
	if task == 'predictors':
		print('\nInitiating Predictors\n')
		initiatePredictors()
		return "poop"
	elif task == 'check':
		initiateCheck()
		return "poop"


	# elif task == "scrape":
	# elif task == "condense":
	# elif task == 'current':
	# elif task == 'predict'
	# elif task == 'check'

# @app.route('/updates/<botID>/<task>/<company>/<index>')
# def index(botID, task, company, index):
@app.route('/complete/<botID>', methods=['GET'])
def complete(botID):
	global tasks
	global progress

	tasks.remove(bots[botID])
	progress.remove(bots[botID])
	assignBot(botID)
	return "poop"

@app.route('/update/<botID>/<task>', methods=['GET'])
def update(botID, task):
	
	bots[botID] = task

	return "here"


if __name__ == "__main__":
    app.run(debug=True)