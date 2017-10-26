from selenium.webdriver.common.keys import Keys
import selenium.webdriver
import time
from bs4 import BeautifulSoup 
import urllib3
import re
import certifi
import re
# import scraper
# import stockeval
# import condenser
import os
from datetime import date, timedelta,datetime
import spacy
from spacy.parts_of_speech import ADV
import shutil
# import scraper2

# class Ticker()



# class PredictorManager()

def getHtml(url):
	http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
	response = http.request('GET', url)
	soup = BeautifulSoup(response.data,"lxml")
	return soup

def getTargets():

	targets = []
	for line in open('./targets.txt').readlines():
		targets.append(line.strip())

	return targets

def getExtended():
	extended = []
	for line in open('./extended.txt').readlines():
		extended.append(line.strip())

	return extended



def resetAllStatus():
	for ticker in os.listdir('./companies'):
		out = open('./Companies/{}/info.txt'.format(ticker), 'w')
		out.write("None")
		out.close()

def main():

	poop = 3

main()