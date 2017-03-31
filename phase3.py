from bsddb3 import db
import re 
import sys
import time
import os

def main():
	#RUNNING = True
		
	while True:
		choice = input("Enter query or exit: ").strip().lower()
		if(choice == "exit"):
			#RUNNING = False
			break
		else:
			getQueries(choice)

def getQueries(choice):
	queries = choice.split()
	for query in queries:
		#Not full validation - a date of 2010/13/35 will just search the terms without warning
		if(re.match("date[:|<|>][0-9]{4}/[0|1]{1}[0-9]{1}/[0-3]{1}[0-9]{1}", query) is not None):
			parseDate(query)
		elif(re.match("[0-9]{4}/[0|1]{1}[0-9]{1}/[0-3]{1}[0-9]{1}", query) is not None):
			parseDate(query)
		else:
			parseTerm(query.strip())

def parseDate(date):
	#Iterates through the index file for the dates. If it finds
	# the date that matches, it will getTweet using the TweetID
	modifer = None
	validDate = re.findall("[0-9]{4}/[0|1]{1}[0-9]{1}/[0-3]{1}[0-9]{1}", date)
	newDate = time.strptime(validDate[0], "%Y/%m/%d")
	if(":" in date or "<" in date or ">" in date):
		modiferList = re.findall("[<|>|:]", date)
		modifer = modiferList[0]
	dateDatabase = db.DB()
	dateDatabase.open("da.idx")
	dateCursor = dateDatabase.cursor()
	iterator = dateCursor.first()
	tweetList = []
	while iterator:
		tweetDate = iterator[0]
		tweetID = iterator[1]
		tempDate = time.strptime(tweetDate.decode("utf-8"), "%Y/%m/%d")
		if(modifer == ":" or modifer == None):
			if(newDate == tempDate):
				tweetList.append(getTweet(tweetID.decode("utf-8")))
		elif(modifer == ">"):
			#This returns all dates larger than the entered date
			if(newDate < tempDate):
				tweetList.append(getTweet(tweetID.decode("utf-8")))
		elif(modifer == "<"):
			#This returns all dates smaller than the entered date
			if(newDate > tempDate):
				tweetList.append(getTweet(tweetID.decode("utf-8")))
		iterator = dateCursor.next()
	dateCursor.close()
	dateDatabase.close()
	formatData(tweetList)

#Retrieve the tweet with the matching ID
def getTweet(tweetID):
	tweetDatabase = db.DB()
	tweetDatabase.open("tw.idx")
	tweetCursor = tweetDatabase.cursor()
	encodedID = tweetID.encode("utf-8")
	tempData = tweetDatabase.get(encodedID).decode("utf-8")	
	tweetDatabase.close()
	tweetCursor.close()
	return tempData

#The option menu is manipulated here
def formatData(tweetList):
	amount = len(tweetList)
	counter = 0
	os.system("clear")
	if(amount == 0):
		FLAG = False
	else:
		FLAG = True
		dataPrinter(tweetList[counter])
	print("\n %d Option(s)" %amount)
	if(amount > 1):
		command = input("n To see Another or exit: ").strip().lower()
		if(command == "exit"):
			FLAG = False
		while (FLAG):
			if(command == 'n'):
				counter += 1
				if(counter >= amount):
					print("No more to see")
					break
				else:
					os.system("clear")
					print("%d/%d" %(counter+1, amount))
					dataPrinter(tweetList[counter])
					command = input("Press n To See Another: ").strip().lower()
			elif(command == "exit"):
				FLAG = False
				break
			else:
				command = input("Enter a Valid Option: ").strip().lower()
				


def parseTerm(term):	
	nameQuery = None
	textQuery = None
	locationQuery = None
	query = None
	partial = False
	
	if (term[-1] == '%'):
		partial = True

	if(":" in term):
		text = term.split(":")
		if(text[0] ==  "name"):
			query = "n-" + text[1]
		elif(text[0] == "text"):
			query = "t-" + text[1]
		elif(text[0] == "location"):
			query = "l-" + text[1]
	else:
		nameQuery = "n-" + term
		textQuery = "t-" + term
		locationQuery = "l-" + term

	if(nameQuery != None):
		runQuery(nameQuery, partial)
	if(textQuery != None):
		runQuery(textQuery, partial)
	if(locationQuery != None):
		runQuery(locationQuery, partial)
	if(query != None):
		runQuery(query, partial)
	


def runQuery(query, partial):
	termDatabase = db.DB()
	termDatabase.open("te.idx")
	termCursor = termDatabase.cursor()
	iterator = termCursor.first()
	
	if partial:
		query = query[:-1]

	tweetList = []
	while iterator:
		if partial:
			if(re.fullmatch(query + ".*", iterator[0].decode("utf-8")) != None):
				tweetID = iterator[1].decode("utf-8")
				tempTweet= getTweet(tweetID)
				if(tempTweet not in tweetList):
					tweetList.append(tempTweet)
		else:
			if(iterator[0].decode("utf-8") == query):
				tweetID = iterator[1].decode("utf-8")
				tempTweet= getTweet(tweetID)
				if(tempTweet not in tweetList):
					tweetList.append(tempTweet)

		iterator = termCursor.next()
	formatData(tweetList)


#Prints the data in a human-readable format 
def dataPrinter(data):
	recordID = re.findall("<id>(.*?)<\/id>", data)[0]
	recordDate = re.findall("<created_at>(.*?)<\/created_at>", data)[0]
	recordText = re.findall("<text>(.*?)<\/text>", data)[0]
	count = re.findall("<retweet_count>(.*?)<\/retweet_count>", data)[0]
	name = re.findall("<name>(.*?)<\/name>", data)[0]
	location = re.findall("<location>(.*?)<\/location>", data)[0]
	desc = re.findall("<description>(.*?)<\/description>", data)[0]
	url = re.findall("<url>(.*?)<\/url>", data)[0]
	print("\n")
	print("ID: " + recordID)
	print("Date: " + recordDate)
	print("Text: " + recordText)
	print("Retweet Count: " + count)
	print("Name: " + name)
	print("Location: " + location)
	print("Description: " + desc)
	print("URL: " + url)
	print("\n")





main()
