import math
import operator
from scipy import spatial
import os
import StockBot
import urllib3
import urllib.request as urllib
from bs4 import BeautifulSoup 
import certifi
from bot import bot

def getHtml(url):
	http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), timeout = 5.0)
	response = http.request('GET', url)
	soup = BeautifulSoup(response.data,"html5lib")
	return soup

def stringMonth(month):
	month = int(month)
	if month == 1:
		return "jan"
	elif month == 2:
		return "feb"
	elif month == 3:
		return "mar"
	elif month == 4:
		return "apr"
	elif month == 5:
		return "may"
	elif month == 6:
		return "jun"
	elif month == 7:
		return "jul"
	elif month == 8:
		return "aug"
	elif month == 9:
		return "sep"
	elif month == 10:
		return "oct"
	elif month == 11:
		return "nov"
	elif month == 12:
		return "dec"
	else:
		return None


class Date(object):
	def __init__(self, month,day,year):
		self.month = int(month)
		self.day = int(day)
		self.year = int(year)

	def __eq__ (self, other):
		return (self.month == other.month and self.day == other.day and self.year == other.year)

	def __ne__ (self, other):
		return (self.month != other.month or self.day != other.day or self.year != other.year)

	def __lt__ (self, other):

		if self.year != other.year:
			if self.year < other.year:
				return True
			else:
				return False

		elif self.month != other.month:
			if self.month < other.month:
				return True
			else:
				return False

		elif self.day != other.day:
			if self.day < other.day:
				return True
			else:
				return False
		else:
			return False

	def __le__ (self, other):
		if self.year != other.year:
			if self.year < other.year:
				return True
			else:
				return False

		elif self.month != other.month:
			if self.month < other.month:
				return True
			else:
				return False

		elif self.day != other.day:
			if self.day < other.day:
				return True
			else:
				return False
		else:
			return True

	def __gt__ (self, other):
		if self.year != other.year:
			if self.year > other.year:
				return True
			else:
				return False

		elif self.month != other.month:
			if self.month > other.month:
				return True
			else:
				return False

		elif self.day != other.day:
			if self.day > other.day:
				return True
			else:
				return False
		else:
			return False

	def __ge__ (self, other):
		if self.year != other.year:
			if self.year > other.year:
				return True
			else:
				return False

		elif self.month != other.month:
			if self.month > other.month:
				return True
			else:
				return False

		elif self.day != other.day:
			if self.day > other.day:
				return True
			else:
				return False
		else:
			return True

	def getDirection(self, term):
		try:
			data = open('./Companies/{}/history/{}-{}-{}.txt'.format(term, self.month, self.day, self.year))
			opening = float(data[0].strip())
			closing = float(data[1].strip())
			if closing -opening >0:
				return "positive"
			else:
				return 'negative'
		except:
			direction = None
		try:
			direction = self.getD1(term)
		except:
			direction = None

		if direction == None:
			try:
				direction = self.getD2(term)
			except:
				direction = None

		return direction
	
	def getD1(self,term):
		parsed = [str(self.month), str(self.day), str(self.year)]
		percent = '%'
		soup = getHtml('http://bigcharts.marketwatch.com/historical/default.asp?symb={}&closeDate={}{}2F{}{}2F{}'.format(term, parsed[0],percent,parsed[1],percent,parsed[2][-2:]))
		table = soup.find("table", id = "historicalquote")
		trs = table.find_all('tr')
		closing = trs[2].find("td").text.strip().replace(',','')
		opening = trs[3].find("td").text.strip().replace(',','')
		high = trs[4].find("td").text.strip().replace(',','')
		low = trs[5].find("td").text.strip().replace(',','')
		change = float(closing)-float(opening)
		if change>0:
			return "positive"
		else:
			return "negative"

	def getD2(self,term):
		driver = bot.DriverManager()
		driver.get('https://www.google.com/finance/historical?q={}'.format(term))

		datestring = '{} {}, {}'.format(stringMonth(self.month), self.day, self.year)
		driver.driver.find_element_by_xpath("//input[@name='startdate'][@type='text']").clear()
		driver.driver.find_element_by_xpath("//input[@name='startdate'][@type='text']").send_keys(datestring)
		driver.driver.find_element_by_xpath("//input[@name='enddate'][@type='text']").clear()
		driver.driver.find_element_by_xpath("//input[@name='enddate'][@type='text']").send_keys(datestring)
		driver.driver.find_element_by_xpath("//input[@id='hfs'][@type='submit']").click()

		soup = driver.getSoup()

		try:
			table = soup.find('table', class_='gf-table historical_price')

			tds = table.find_all('td', class_ = 'rgt')

			opening = float(tds[0].text.strip().replace(',',''))
			high = float(tds[1].text.strip().replace(',',''))
			low = float(tds[2].text.strip().replace(',',''))
			closing = float(tds[3].text.strip().replace(',',''))
			driver.driver.close()

			if closing - opening >0:
				return "positive"
			else:
				return 'negative'
		except:
			try:
				driver.driver.close()
			except:
				poop = 3
			return None

		return None

	def getData(self,term):
		try:
			data = self.getData1(term)
		except:
			data = None

		if data == None:
			try:
				data = self.getData2(term)
			except:
				data = None


		out = open('./Companies/{}/history/{}-{}-{}.txt'.format(term, self.month, self.day, self.year), 'w')
		if data == None:
			out.write("none")
		else:
			for point in data:
				out.write(point+'\n')

	def getData1(self,term):
		parsed = [str(self.month), str(self.day), str(self.year)]
		percent = '%'
		soup = getHtml('http://bigcharts.marketwatch.com/historical/default.asp?symb={}&closeDate={}{}2F{}{}2F{}'.format(term, parsed[0],percent,parsed[1],percent,parsed[2][-2:]))
		table = soup.find("table", id = "historicalquote")
		trs = table.find_all('tr')
		closing = trs[2].find("td").text.strip().replace(',','')
		opening = trs[3].find("td").text.strip().replace(',','')
		high = trs[4].find("td").text.strip().replace(',','')
		low = trs[5].find("td").text.strip().replace(',','')
		return [opening,closing,high,low]

	def getData2(self,term):
		driver = bot.DriverManager()
		driver.get('https://www.google.com/finance/historical?q={}'.format(term))

		datestring = '{} {}, {}'.format(stringMonth(self.month), self.day, self.year)
		driver.driver.find_element_by_xpath("//input[@name='startdate'][@type='text']").clear()
		driver.driver.find_element_by_xpath("//input[@name='startdate'][@type='text']").send_keys(datestring)
		driver.driver.find_element_by_xpath("//input[@name='enddate'][@type='text']").clear()
		driver.driver.find_element_by_xpath("//input[@name='enddate'][@type='text']").send_keys(datestring)
		driver.driver.find_element_by_xpath("//input[@id='hfs'][@type='submit']").click()

		soup = driver.getSoup()

		try:
			table = soup.find('table', class_='gf-table historical_price')

			tds = table.find_all('td', class_ = 'rgt')

			opening = float(tds[0].text.strip().replace(',',''))
			high = float(tds[1].text.strip().replace(',',''))
			low = float(tds[2].text.strip().replace(',',''))
			closing = float(tds[3].text.strip().replace(',',''))
			driver.driver.close()

			return [opening,closing,high,low]
		except:
			try:
				driver.driver.close()
			except:
				poop = 3
			return None

		return None


def recordSoup(soup):
	file = open('./out.txt', 'w')
	for i in str(soup):
		try:
			file.write(i)
		except:
			poop = 2
	file.close()

class Cluster(object):
	def __init__(self, article):
		self.articles = [article]
		self.center = article

	def add(self, article):
		self.articles.append(article)
		self.recenter()

	def recenter(self):
		best = 0
		new_center = None
		for i,article in enumerate(self.articles):
			score = 0
			for j,check in enumerate(self.articles):
				if j == i:
					continue
				else:
					score += article.compare(check)

			score = score/float(len(self.articles)-1)

			if score >best:
				best = score
				new_center = article

		self.center = new_center


class Company(object):
	def __init__(self,ticker):
		self.ticker = ticker

	def updatePriceHistory(self):
		targetDir = "./Companies/{}/history/".format(self.ticker)
		if 'history' not in os.listdir( "./Companies/{}/".format(self.ticker)):
				os.mkdir(targetDir)
		for date in os.listdir("./Companies/{}/predictors/".format(self.ticker)):
			if date not in os.listdir(targetDir):
				parsed = date.split('-')

				if len(parsed) != 3:
					continue
				temp = Date(parsed[0], parsed[1], parsed[2])
				temp.getData(self.ticker)


	def loadClusters(self):
		self.clusters = []
		targetDir = './Companies/{}/clusters/'.format(self.ticker)
		for file in os.listdir(targetDir):
			data = open(targetDir+file).readlines()
			cluster = Cluster(Article(data[0].strip()))

			for i,line in enumerate(data):
				if i == 0:
					continue
				cluster.articles.append(Article(line.strip()))
			if len(cluster.articles)>1:
				cluster.recenter()
			self.clusters.append(cluster)


	def createClusters(self):
		#loads the predictors data
		self.loadPredictors()

		#preps all articles for comparison with eachother
		master = self.articles[0]
		for i,article in enumerate(self.articles):
			if i == 0:
				continue
			else:
				master.prep(article)

		print("master prepped")

		for article in self.articles:
			article.prep(master)


		print("prepped")

		#initiates the clusters
		self.clusters = []
		for article in self.articles:
			print(article.path)
			if len(self.clusters) == 0:
				self.clusters.append(Cluster(article))
				continue
			selected = None
			best = 0
			for cluster in self.clusters:
				score = article.compare(cluster.center)
				if score >best:
					best = score
					if score >.7:
						selected = cluster
			if selected == None:
				self.clusters.append(Cluster(article))
			else:
				selected.add(article)


	def loadPredictions(self):
		self.predictions = {}
		self.predictions2 = {}
		self.legacypredictions = {}
		self.legacypredictions2 = {}

		self.getPredictionData(self.predictions,'predictions')
		self.getPredictionData(self.predictions2,'predictions2')
		self.getPredictionData(self.legacypredictions,'legacypredictions')
		self.getPredictionData(self.legacypredictions2,'legacypredictions2')

	def getPredictionData(self, dictionary, filename):
		data = open('./Companies/{}/{}.txt'.format(self.ticker, filename)).readlines()

		for line in data: 
			date = line.split(":")[0].strip()
			prediction = line.split(":")[1].split(",")[0].strip()
			confidence = float(line.split(":")[1].split(",")[1].strip())

			direction = self.getDirection(date)

			if direction == None:
				print('Get = for {} on {}'.format(self.ticker, date))
				continue

			dictionary[date] = {'prediction':prediction,'confidence':confidence, 'direction':direction}

	def getDirection(self, date):
		month, day, year = date.split('-')
		temp = Date(month, day, year)
		return temp.getDirection(self.ticker)

	def getWords(self):
		self.loadPredictors()
		article = None
		for temp in self.articles:
			if article == None:
				article = temp
			else:
				article.prep(temp)

		words = []
		for word in article.counts:
			words.append(word)

		return words

	def getNames(term):
		data = open('./sp500.txt','r').readlines()
		for line in data:
			parsed = line.strip().split(",")
			if term == parsed[0].strip():
				parsed.remove(term)
				return(parsed)
		return names

	def loadPredictors(self):
		self.articles = []

		predictorPath = './Companies/{}/predictors/'.format(self.ticker)

		folders = os.listdir(predictorPath)

		if "History" in folders:
				folders.remove('History')
		for folder in folders:
			files = os.listdir(predictorPath+folder)
			if len(files) == 0:
				continue
			for file in files:
				if len(open(predictorPath+folder+'/'+file).readlines()) <3:
					os.remove(predictorPath+folder+'/'+file)
				else:
					self.articles.append(Article(predictorPath+folder+'/'+file))


class Article(object):
	def __init__(self,articlePath):

		self.path = articlePath
		data = open(self.path).readlines()
		# print(data)
		
		self.url = data[0].strip()
		self.source = data[1].strip()

		month,day,year = data[2].strip().split('/')
		self.date = Date(month,int(day)+1,year)

		
		self.counts = {}
		for line in data[3:]:
			self.counts[line.split(",")[0].strip()] = int(line.split(",")[1].strip())
	def reload(self):
		data = open(self.path).readlines()
		self.counts = {}
		for line in data[3:]:
			self.counts[line.split(",")[0].strip()] = int(line.split(",")[1].strip())

	def prep(self, other):
		for word in other.counts:
			if word not in self.counts:
				self.counts[word]= 0
		for word in self.counts:
			if word not in other.counts:
				other.counts[word]= 0

	def compare(self, other):
		# if len(self.counts) != len(other.counts):
		self.prep(other)

		v1 = []
		v2 = []

		for word in sorted(self.counts):
			v1.append(self.counts[word])
			v2.append(other.counts[word])

		return cosineSimilarity(v1,v2)

def dotProduct(v1, v2):
    return sum(map(operator.mul, v1, v2))


def cosineSimilarity(v1, v2):
    prod = dotProduct(v1, v2)
    len1 = math.sqrt(dotProduct(v1, v1))
    len2 = math.sqrt(dotProduct(v2, v2))
    return prod / (len1 * len2)

def checkAccuracy():
	companies = []
	for target in StockBot.getTargets(): companies.append(Company(target))
	for company in companies: company.loadPredictions()

	right = 0
	wrong = 0
	right2 = 0
	wrong2 = 0

	for test in companies:
		print(test.ticker)
		test.loadPredictions()
		for date in test.predictions:

			#shitty logic to exclude dates
			forbidden = ['8-21-2017','8-22-2017','8-23-2017','8-24-2017','8-25-2017']
			if date in forbidden:
				continue

			if test.predictions[date]['confidence'] <3:
				continue
			if test.predictions[date]['prediction'] == test.predictions[date]['direction']:
				right +=1
			else:
				wrong +=1

		for date in test.predictions2:
			if test.predictions2[date]['confidence'] <3:
				continue
			if test.predictions2[date]['prediction'] == test.predictions2[date]['direction']:
				right2 +=1
			else:
				wrong2 +=1

		print("\nPredictions:")
		print(str(right/(right+wrong)*100) +"%")

		print("\nPredictions 2:")
		print(str(right/(right+wrong)*100) +"%")

	print("\nFINAL:\nPredictions:")
	print(str(right/(right+wrong)*100) +"%")

	print("\nFINAL:\nPredictions 2:")
	print(str(right/(right+wrong)*100) +"%")

def getAllClusters():
	targets = StockBot.getTargets()
	if bot.PCID() == "Yoda":
		targets = reversed(targets)
	for target in targets:
		getClusters(target)

def getClusters(target):
	print(target)
	test = Company(target)
	test.createClusters()
	targetDir = "./Companies/{}/clusters/".format(target)
	os.mkdir(targetDir)
	for cluster in test.clusters:
		out = open(targetDir+'{}.txt'.format(len(os.listdir(targetDir))+1),'w')
		for article in cluster.articles:
			out.write(article.path+'\n')
		out.close()

def main():

	poop = False
	while poop != 'penis':
		poop = input("Enter the stock ticker: ")
		try:
			getClusters(poop)
		except:
			penis = 2

	# getAllClusters()
	# for target in StockBot.getTargets():
	# 	print(target)
	# 	test = Company(target)
	# 	test.updatePriceHistory()

	# test = Company('AIG')
	# test.loadClusters()

	# for cluster in test.clusters:
	# 	if len(cluster.articles) >3:
	# 		print('\n')
	# 		for article in cluster.articles:
	# 			print(article.path)
	# 			print(article.date.getDirection(test.ticker))


	
	# print(test.getDirection('7-31-2017'))
	# date = Date(9,1,2017)
	# print(date.getD2('AIG'))
	# print(date.getDirection('aig'))

	

	


	# right = 0
	# wrong = 0
	# for date in test.predictions2:
	# 	if test.predictions2[date]['confidence'] <3:
	# 		continue
	# 	if test.predictions2[date]['prediction'] == test.predictions2[date]['direction']:
	# 		right +=1
	# 	else:
	# 		wrong +=1
	# print("predictions2")
	# print(str(right/(right+wrong)*100) +"%")

	# right = 0
	# wrong = 0
	# for date in test.legacypredictions:
	# 	if test.legacypredictions[date]['confidence'] <3:
	# 		continue
	# 	if test.legacypredictions[date]['prediction'] == test.legacypredictions[date]['direction']:
	# 		right +=1
	# 	else:
	# 		wrong +=1
	# print("legacypredictions")
	# print(str(right/(right+wrong)*100) +"%")

	# right = 0
	# wrong = 0
	# for date in test.legacypredictions2:
	# 	if test.legacypredictions2[date]['confidence'] <3:
	# 		continue
	# 	if test.legacypredictions2[date]['prediction'] == test.legacypredictions2[date]['direction']:
	# 		right +=1
	# 	else:
	# 		wrong +=1
	# print("legacypredictions2")
	# print(str(right/(right+wrong)*100) +"%")



	# dates = {}
	# for target in StockBot.getTargets():
	# 	company = Company(target)
	poop = 3
	# words = []
	# for target in StockBot.getTargets():
	# 	company = Company(target)
	# 	words = company.getWords()

	# company = Company("AIG")
	# words1 = company.getWords()
	# company2 = Company("PFE")
	# words2 = company2.getWords()
	# company3 = Company("PG")
	# words3 = company3.getWords()

	# intersection = []
	# for word in words1:
	# 	if word in words2 and word in words3:
	# 		intersection.append(word)
	# print(len(words1))
	# print(len(words2))
	# print(len(intersection))

	# a1 = Article('C:/Users/vamsh/OneDrive/Bots/StockBot/Companies/PG/predictors/8-23-2017/34.txt')
	# a2 = Article('C:/Users/vamsh/OneDrive/Bots/StockBot/Companies/PG/predictors/8-23-2017/51.txt')

	# print(a1.compare(a2))
main()
