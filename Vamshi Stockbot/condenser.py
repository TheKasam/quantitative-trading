#Beautiful Soup is a Python library for pulling data out of HTML and XML files.
from bs4 import BeautifulSoup
#http client for python
import urllib3
import time
#interacting with folders / dir
import os
#Natural Language Processing
import spacy
from spacy.parts_of_speech import ADV
from bot import bot
import random

#turns debugmode on or off:
debug = False

#initializes the natural language processor
global nlp
nlp = spacy.load('en')

#A set to hold the cache data
global cached
cached = set()

#initializes path variables to find local files

global antPath
global synPath
global currentPath
global storagePath
global cachePath
global rootPath

storagePath = './Companies/'


rootPath = bot.getRootPath()
antPath = rootPath+'Memory/antonyms/'
synPath = rootPath+'Memory/synonyms/'
currentPath = bot.getPath()

cachePath = rootPath +'Memory/cache/'

#just making sure file is being opened and has content in it.
def realOpen(filePath):
	for i in range(5):
		file = open(filePath)
		if file.readline().strip() != "":
			file.seek(0)
			return file
	file.seek(0)
	return file

class Thesaurus(object):
	def __init__(self):
		self.antDict = {}
		self.synDict = {}

		for antonym in os.listdir(antPath):
			rawAnt = realOpen(antPath+'{}'.format(antonym)).readline().strip()
			if rawAnt != "":
				self.antDict[antonym[:-4]] = rawAnt


		for synonym in os.listdir(synPath):
			data = realOpen(synPath+'{}'.format(synonym)).readlines()
			if len(data)!=0:
				temp = []
				for line in data:
					temp.append(line.strip())
				self.synDict[synonym[:-4]] = temp

	def updateDicts(self,cache):
		cacheID = cache[:-4]
		try:
			synType , word = realOpen(cachePath+cache).readline().strip().split(',')
		except:
			try:
				os.remove(cachePath+cache)
				return
			except:
				return


		if synType == "syn":
			data = open(synPath+word+'.txt').readlines()
			if len(data) == 0:
				return
			temp = []
			for line in data:
				temp.append(line.strip())
			self.synDict[word] = temp

		elif synType == "ant":
			data = open(antPath+word+'.txt').readline()
			if data.strip == "":
				return
			self.antDict[word] =data.strip()

		try:
			cacheCount = int(realOpen(cachePath+cache).readlines()[1].strip()) +1
		except:
			return

		numBots = int(open(rootPath+'Memory/numBots.txt').readline().strip())

		if cacheCount >= numBots:
			i = 0
			while 2>1:
				try:
					i +=1
					os.remove(cachePath+cache)
					break
				except:
					if i>50:
						print(i)
					continue
				break
			if debug:
				print("removed cache {}".format(cache))
		else:
			outfile = open(cachePath+cache, 'w')
			outfile.write("{},{}\n".format(synType,word))
			outfile.write(str(cacheCount))
			cached.add(cacheID)

	def refresh(self):
		caches = os.listdir(cachePath)
		for cache in caches:
			cacheID = cache[:-4]
			if cacheID not in cached:
				self.updateDicts(cache)

		# self.antDict = {}
		# self.synDict = {}

		# for antonym in os.listdir(antPath):
		# 	# rawAnt = realOpen(antPath+'{}'.format(antonym)).readline().strip()
		# 	rawAnt = open(antPath+'{}'.format(antonym)).readline().strip()

		# 	if rawAnt != "":
		# 		self.antDict[antonym[:-4]] = rawAnt


		# for synonym in os.listdir(synPath):
		# 	# data = realOpen(synPath+'{}'.format(synonym)).readlines()
		# 	data = open(synPath+'{}'.format(synonym)).readlines()
		# 	if len(data)==0:
		# 		continue
		# 	temp = []
		# 	for line in data:
		# 		temp.append(line.strip())
		# 	self.synDict[synonym[:-4]] = temp

global t
t = Thesaurus()

def getAntDict():
	return t.antDict
def getSynDict():
	return t.synDict


def getHtml(url):
	http = urllib3.PoolManager()
	response = http.request('GET', url)
	soup = BeautifulSoup(response.data,"html5lib")
	return soup

def cache(synType, word):
	duplicate = True
	cacheID = 0
	while duplicate:
		duplicate = False
		cacheID = random.randrange(1,200000)
		for file in os.listdir(cachePath):
			check = file[:-4]
			try:
				if int(check) == cacheID:
					duplicate = True
			except:
				ui = 3
	file = open(cachePath+'{}.txt'.format(cacheID), 'w')
	file.write('{},{}\n'.format(synType, word))
	file.write('0')
	file.close()

	cached.add(cacheID)

def addSynonym(word, synonym):
	synonyms = t.synDict[word]
	if synonym in synonyms:
		return
	else:
		t.synDict[word] = synonyms.append(synonym)
		new = open(synPath+'{}.txt'.format(word), "w")
		for synonym in synonyms:
			new.write(synonym+'\n')
		cache("syn", word)


def addAntonym(word):
	http = urllib3.PoolManager()

	url = "http://www.synonym.com/synonyms/"+word
	response = http.request('GET', url)
	soup = BeautifulSoup(response.data,"lxml")
	x = soup.find_all("div", class_ = "synonym")
	largest = 0
	antonyms = []

	for poop in x:
		raw = poop.h3.text
		parsed = raw[raw.index("(")+1:raw.index(")")-1]

		if parsed != "adj":
			continue
		else:
			uls = poop.find_all("ul")
			syns = uls[0].find_all("li")

			if len(syns)>largest:
				oldLargest = largest
				largest = len(syns)
				antonyms = []

				try:
					rawants = uls[1].find_all("li")
					for ant in rawants:
						antonyms.append(ant.text.strip())
				except:
					largest = oldLargest

	most = 0
	best = ""

	alts = antonyms
	none = True

	# print("These are the alts")
	# print(alts)

	for p in alts:
		if p != None:
			none = False
		if checkWord(p) == False:
			continue
		syns = getAlts(p)
		if syns == None:
			continue
		# print(p)
		# print(len(getSynonyms(p)))
		end = ""
		ecount = 0
		okay = True
		for check in syns:
			temp = check[-2:]
			if end == temp:
				ecount +=1
			else:
				ecount= 0
			end = temp
			if ecount == 5:
				okay = False
				break

		if okay and len(syns) > most:
			most = len(syns)
			best = p

	# print(s)
	if none:
		new = open(antPath+'{}.txt'.format(word), "w")
		new.write("not "+word)
		new.close()
		t.antDict[word] = "not "+word

		cache("ant", word)
	else:
		addWord2(best,word,antonyms)
	return best


def getAlts(word):
	http = urllib3.PoolManager()

	url = "http://www.synonym.com/synonyms/"+word
	response = http.request('GET', url)
	soup = BeautifulSoup(response.data,"lxml")

	if soup.find(id="notification") != None:
		return None

	synonyms = []

	x = soup.find_all("h3")
	largest = 0
	for h in x:
		raw = h.text
		parsed = raw[raw.index("(")+1:raw.index(")")-1]
		if parsed != "adj":
			continue
		else:
			ul = h.next.next.next.next.next.next.next
			syns = ul.find_all("li")
			if len(syns)>largest:
				largest = len(syns)
				synonyms = []
				for syn in syns:
					if syn != None:
						synonyms.append(syn.text.strip())

	return sorted(synonyms)

def getSynonyms(word):
	try:
		if word in t.synDict:
			return t.synDict[word]
		else:
			http = urllib3.PoolManager()
			count = 0
			synonyms = []
			url = "http://www.synonym.com/synonyms/"+word
			response = http.request('GET', url)
			soup = BeautifulSoup(response.data,"lxml")
			x = soup.find_all("li")
			for tag in x:
				if tag["class"] == ['syn']:
					synonyms.append(tag.text.strip())
					count +=1

			return sorted(synonyms)
	except:
		return None

def addWord(word):
	if word== None:
		return
	new = open(synPath+'{}.txt'.format(word), "w")

	http = urllib3.PoolManager()

	url = "http://www.synonym.com/synonyms/"+word
	response = http.request('GET', url)
	soup = BeautifulSoup(response.data,"lxml")
	x = soup.find_all("li")
	synonyms = []
	for tag in x:
		if tag["class"] == ['syn']:
			synonyms.append(tag.text.strip())
			new.write(tag.text.strip()+'\n')
	new.close()

	t.synDict[word] = synonyms
	cache('syn', word)

	addAntonym(word)


def addWord2(word,antonym,synonyms):
	new = open(synPath+'{}.txt'.format(word), "w")

	for syn in synonyms:
		new.write(syn+'\n')

	http = urllib3.PoolManager()

	url = "http://www.synonym.com/synonyms/"+word
	response = http.request('GET', url)
	soup = BeautifulSoup(response.data,"lxml")
	x = soup.find_all("li")
	for tag in x:
		if tag["class"] == ['syn']:
			new.write(tag.text.strip()+'\n')
	new.close()


	cache("syn", word)

	new = open(antPath+'{}.txt'.format(word), "w")
	new.write(antonym)
	new.close()

	cache("ant", word)

def getAntonym(word):
	if word in t.antDict:
		return t.antDict[word]
	else:
		return 'not '+word

def isAdj(word):
	soup = getHtml('http://www.synonym.com/synonyms/'+word)
	raw = soup.find("h3").text.strip()
	parsed = raw[raw.index("(")+1:raw.index(")")-1]
	return  parsed == "adj"

def checkWord(word):
	bad = ['?',"/","(",")",".",",","$","#","@","*","%","1","2","3","4","5","6","7","8","9","0"]
	for i in word:
		if i in bad:
			return False
		if i.isalpha() == False:
			if i != "-":
				return False
	if word[0] == "-" or word[-1] == "-":
		return False

	generic = ['be','have', 'will']
	if word in generic:
		return False

	return True

def condense(text):
	global nlp
	notModifier = False
	doc = nlp(text)
	wordlist = []

	for word in doc:
		# print("next word")
		t.refresh()
		#to skip words that arent actually words
		if checkWord(word.lemma_) == False:
			continue

		lemma = word.lemma_.strip()
		pos = word.pos_.strip()

		if lemma == "not":
			notModifier = True
		elif pos == "VERB":
			wordlist.append(lemma)
			notModifier = False
		elif pos == "PROPN":
			wordlist.append(word.text.strip())
			notModifier = False
		elif pos == "PUNCT" or pos == "NOUN":
			notModifier = False
		elif pos == "ADJ":
			if lemma in t.synDict:
				if notModifier:
					wordlist.append(getAntonym(lemma))
					notModifier = False
				else:
					wordlist.append(lemma)
					notModifier = False
			else:
				check = getSynonyms(lemma)
				if check == None:
					continue
				else:
					found = False
					for c in check:
						if c in t.synDict:
							wordlist.append(c)
							found = True
							break
					if found == False:
						for term in t.synDict:

							synonyms = t.synDict[term]
							try:
								if lemma in synonyms:
									wordlist.append(term)
									found = True
									break
								else:
									continue
							except:
								continue
					if found == False:
						s = getSynonyms(lemma)
						most = len(s)
						best = lemma
						alts = getAlts(lemma)

						if alts == None:
							pooasdf = 90
						else:
							for p in alts:
								if checkWord(p) == False:
									continue

								for c in p:
									if not c.isalpha():
										continue

								syns = getAlts(p)

								if syns == None:
									continue

								end = ""
								ecount = 0
								okay = True
								for check in syns:
									temp = check[-2:]
									if end == temp:
										ecount +=1
									else:
										ecount= 0
									end = temp
									if ecount == 5:
										okay = False
										break


								if okay and len(syns) > most:
									most = len(syns)
									best = p
						# print(s)
						if best in t.synDict:
							addSynonym(best,lemma)
							if notModifier:
								wordlist.append(getAntonym(best))
								notModifier = False
							else:
								wordlist.append(best)
						else:
							addWord(best)
							addSynonym(best,lemma)
							if notModifier:
								wordlist.append(getAntonym(best))
							else:
								wordlist.append(best)

	for item in wordlist:
		if item == None:
			wordlist.remove(item)

	return wordlist

def sortWords(words):
    words.sort()
    wordList = {}
    i = 0
    while i < len(words):
        w = words[i]
        if w not in wordList:
            wordList[w] = 1
        else:
            current = wordList[w]
            wordList[w] = current + 1
        i+=1
    final = []
    for key, val in wordList.items():
        temp = [key, val]
        final.append(temp)
    return final

def run(term, start):
	global storagePath
	global nlp
	nlp = nlp
	print("Condensing "+term)
	if start == 0:
		bot.scrub(storagePath+'{}/condensed/'.format(term))

	# articles = os.listdir(storagePath+'{}/raw/'.format(term))
	# print(len(articles))
	# if len(articles)<70:
	# 	if debug : print("scrubbing {}:".format(term))
	# 	bot.scrub(storagePath+'{}'.format(term))
	# 	if debug : print("scrubbed")
	# 	return

	rawPath = storagePath+term+'/raw/'
	outPath = storagePath+term+'/condensed/'
	for file in os.listdir(rawPath):
		if start >0:
			start -= 1
			continue
		if debug:
			print(file)
		# print('Condensing {}/{}'.format(filename[:-4],len(articles)))
		outfile = open(outPath+'{}.txt'.format(len(os.listdir(outPath))+1) , 'w')
		data = open(rawPath+file).readlines()
		if debug:
			print('file manipulation handled')

		if len(data)<5:
			continue

		text = ""
		for i in range(len(data)):
			if i<4:
				outfile.write(data[i])
			else:
				text += (data[i]+' ')

		if debug:
			print('initial info written... about to condense')

		condensed = condense(text)

		if debug:
			print('condensed')

		try:
			towrite = sortWords(condensed)
		except:
			try:
				towrite = sortWords(condensed)
			except:
				towrite = sortWords(condensed)


		for i in towrite:
			outfile.write(i[0]+','+str(i[1])+'\n')

		outfile.close()


def test2():
	data = open('./targets.txt').readlines()
	companies = []
	for line in data:
		companies.append(line.strip())

	# # code to reset
	# for company in companies:
	# 	file = open(currentPath+'companies/{}/info.txt'.format(company), 'w')
	# 	file.write("compiled")
	# 	file.close()
	# return

	if bot.PCID() == "Yoda":
		companies = reversed(companies)

	# skipped = 3
	for company in companies:

		# try:
		if 'raw' not in os.listdir("companies/"+company):
			file = open(currentPath+'companies/{}/info.txt'.format(company), 'w')
			file.write("failed")
			file.close()
			continue

		if open(currentPath+'companies/{}/info.txt'.format(company)).readline().strip() =="done" and len(os.listdir(currentPath+'companies/{}/raw/'.format(company)))>125:
			# if skipped >0:
			# 	skipped -=1
			# 	continue
			file = open(currentPath+'companies/{}/info.txt'.format(company), 'w')
			file.write("do not disturb")
			file.close()
			run(company, 0)
			file = open(currentPath+'companies/{}/info.txt'.format(company), 'w')
			file.write("condensed")
			file.close()
			data = open('./condensed.txt').readlines()
			outfile = open('./condensed.txt', 'w')

			for line in data:
				outfile.write(line)
			outfile.write(company+'\n')
			outfile.close()

		# except:
		# 	file = open(currentPath+'companies/{}/info.txt'.format(company), 'w')
		# 	file.write("failed")
		# 	file.close()
		# 	continue
		# 	data = open('./condensed.txt').readlines()
		# 	outfile = open('./condensed.txt', 'w')

		# 	for line in data:
		# 		outfile.write(line)
		# 	outfile.write(company+'\n')
		# 	outfile.close()

def test():
	data = open('./condensed.txt').readlines()
	condensed =[]
	for line in data:
		condensed.append(line.strip())

	companies = os.listdir(storagePath)

	if bot.PCID() == "Yoda":
		companies = reversed(companies)

	# skipped = 3
	for company in companies:
		# try:
		if 'raw' not in os.listdir("companies/"+company):
			file = open(currentPath+'companies/{}/info.txt'.format(company), 'w')
			file.write("failed")
			file.close()
			continue

		if company not in condensed and open(currentPath+'companies/{}/info.txt'.format(company)).readline().strip() =="done" and len(os.listdir(currentPath+'companies/{}/raw/'.format(company)))>125:
			# if skipped >0:
			# 	skipped -=1
			# 	continue
			file = open(currentPath+'companies/{}/info.txt'.format(company), 'w')
			file.write("do not disturb")
			file.close()
			run(company)
			file = open(currentPath+'companies/{}/info.txt'.format(company), 'w')
			file.write("condensed")
			file.close()
			data = open('./condensed.txt').readlines()
			outfile = open('./condensed.txt', 'w')

			for line in data:
				outfile.write(line)
			outfile.write(company+'\n')
			outfile.close()
			condensed.append(company)
		# except:
		# 	file = open(currentPath+'companies/{}/info.txt'.format(company), 'w')
		# 	file.write("failed")
		# 	file.close()
		# 	continue
		# 	data = open('./condensed.txt').readlines()
		# 	outfile = open('./condensed.txt', 'w')

		# 	for line in data:
		# 		outfile.write(line)
		# 	outfile.write(company+'\n')
		# 	outfile.close()

def resetFailed():
	for term in os.listdir('./Companies'):
		if open('./companies/{}/info.txt'.format(term)).readline() == 'do not disturb':
			file = open('./companies/{}/info.txt'.format(term), 'w')
			file.write("done")
			file.close()

def main():
	toilet = 9
	# # resetFailed()

	# test2()


	# # file = open('C:/Users/Vamshi Gujju/OneDrive/Bots/Memory/cache/42170.txt')
	# # print(file.readline())
	# # file.seek(0)
	# # print(file.readline())


	# # print(t.synDict[])
	# # run('XRX')

	# # print(p)

	# for term in os.listdir('./Companies'):
	# 	available = os.listdir('./Companies/{}'.format(term))
	# 	if 'info.txt' not in available:
	# 		file = open('./Companies/{}/info.txt'.format(term),'w')
	# 		file.write('poop')
	# 		file.close()
	# 	if 'raw' not in available:
	# 		os.mkdir('./Companies/{}/raw'.format(term))
	# 	if 'condensed' not in available:
	# 		os.mkdir('./Companies/{}/condensed'.format(term))
	# 	if 'html' not in available:
	# 		os.mkdir('./Companies/{}/html'.format(term))

main()
