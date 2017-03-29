from bsddb3 import db
import re 
import time

def main():
	RUNNING = True

	while RUNNING:
		choice = input("Enter query or exit: ").strip().lower()
		if(choice.strip() == "exit"):
			RUNNING = False
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
			parseTerm(query)

def parseDate(date):
	#Iterates through the index file for the dates. If it finds
	# the date that matches, it will getTweet using the TweetID
	print("Parsing Date")
	modifer = None
	validDate = re.findall("[0-9]{4}/[0|1]{1}[0-9]{1}/[0-3]{1}[0-9]{1}", date)
	print(validDate)
	newDate = time.strptime(validDate[0], "%Y/%m/%d")
	if(":" in date or "<" in date or ">" in date):
		modiferList = re.findall("[<|>|:]", date)
		modifer = modiferList[0]
	database = db.DB()
	database.open("da.idx")
	cursor = database.cursor()
	iterator = cursor.first()
	while iterator:
		tweetDate = iterator[0]
		tweetID = iterator[1]
		tempDate = time.strptime(tweetDate.decode("utf-8"), "%Y/%m/%d")
		if(modifer == ":" or modifer == None):
			if(newDate == tempDate):
				getTweet(tweetID.decode("utf-8"))
		elif(modifer == ">"):
			#This returns all dates larger than the entered date
			if(newDate < tempDate):
				getTweet(tweetID.decode("utf-8"))
		elif(modifer == "<"):
			#This returns all dates smaller than the entered date
			if(newDate > tempDate):
				getTweet(tweetID.decode("utf-8"))
		iterator = cursor.next()
	cursor.close()
	database.close()


def parseTerm(term):
	print("Parsing Term")


def getTweet(tweetID):
	#TODO - Need to get the tweets from the tweets index file using the tweetID passed in
	print(tweetID)


main()