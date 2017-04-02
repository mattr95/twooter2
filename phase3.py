from bsddb3 import db
import re, sys, time, os

def main():
	while True:
		choice = input("Enter a query or \'exit\': ").strip().lower()
		if(choice == "exit"):
			break
		else:
			tweetSets = getQueries(choice)
			
			# Take intersection of tweetSets
			intersection = tweetSets[0]
			for i in range(1, len(tweetSets)):
				intersection = list(set(intersection) & set(tweetSets[i]))
			
			# Print final list of tweets
			formatData(intersection)

def getQueries(choice):
	tweetSets = [] # list of lists to track query results
	queries = choice.split()
	for query in queries:
		#Not full validation - a date of 2010/13/35 will just search the terms without warning
		if(re.match("date[:|<|>][0-9]{4}/[0|1]{1}[0-9]{1}/[0-3]{1}[0-9]{1}", query) != None):
			tweetSets.append(parseDate(query))
		elif(re.match("[0-9]{4}/[0|1]{1}[0-9]{1}/[0-3]{1}[0-9]{1}", query) != None):
			tweetsSets.append(parseDate(query))
		else:
			tweetSets.append(parseTerm(query.strip()))

	return tweetSets

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
	return tweetList

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
	# os.system("clear")
	# if(amount == 0):
	# 	FLAG = False
	# else:
	# 	FLAG = True
	if (amount > 0):
		dataPrinter(tweetList[counter], counter+1, amount)
	print("\n %d Result(s)" %amount)
	if(amount > 1):
		# command = input("Enter \'n\' to see another result or \'q\' to enter a new query: ").strip().lower()
		# if(command != "q"):
		# 	FLAG = False
		while (True):
			command = input("Enter \'n\' to see another result or \'q\' to enter a new query: ").strip().lower()
			if(command == 'n'):
				counter += 1
				if(counter >= amount):
					print("No more to see")
					break
				else:
					# os.system("clear")
					# print("Result %d/%d" %(counter+1, amount))
					dataPrinter(tweetList[counter], counter+1, amount)
					# command = input("Press n To See Another: ").strip().lower()
			elif(command == 'q'):
				break
			else:
				command = input("Enter a Valid Option (n or q): ").strip().lower()
				


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

	tweetList = []
	if(nameQuery != None):
		tweetList += runQuery(nameQuery, partial)
	if(textQuery != None):
		tweetList += runQuery(textQuery, partial)
	if(locationQuery != None):
		tweetList += runQuery(locationQuery, partial)
	if(query != None):
		tweetList += runQuery(query, partial)

	return tweetList
	

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
	return tweetList


#Prints the data in a human-readable format 
def dataPrinter(data, res_no, n_results):
	recordID = re.findall("<id>(.*?)<\/id>", data)[0]
	recordDate = re.findall("<created_at>(.*?)<\/created_at>", data)[0]
	recordText = re.findall("<text>(.*?)<\/text>", data)[0]
	count = re.findall("<retweet_count>(.*?)<\/retweet_count>", data)[0]
	name = re.findall("<name>(.*?)<\/name>", data)[0]
	location = re.findall("<location>(.*?)<\/location>", data)[0]
	desc = re.findall("<description>(.*?)<\/description>", data)[0]
	url = re.findall("<url>(.*?)<\/url>", data)[0]

	os.system("clear")
	print("Result %d/%d\n" %(res_no, n_results))
	print("ID: " + recordID)
	print("Date: " + recordDate)
	print("Text: " + recordText)
	print("Retweet Count: " + count)
	print("Name: " + name)
	print("Location: " + location)
	print("Description: " + desc)
	print("URL: " + url)
	print("\n")


if __name__ == '__main__':
	main()
