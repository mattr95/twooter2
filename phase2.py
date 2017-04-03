import os
import sys
import re 


#Doesn't ignore /
def main():
	os.system("clear")
	sortFiles()
	createIndex()

def sortFiles():
	os.system("sort -u -o tweets.txt tweets.txt")
	tweets = open("tweets.txt", "r").read()
	tweetKeys = re.findall("[0-9]+(?=:<status>)", tweets)
	print(len(tweetKeys), "entries loaded.\n")
	tweetData = re.findall("<status>.*</status>", tweets) 
	sortedFile = open("sortedTweets.txt", "w")	
	for i in range(len(tweetKeys)):
		sortedFile.write(tweetKeys[i] + "\n")
		sortedFile.write(tweetData[i] + "\n")
	sortedFile.close()


	os.system("sort -u -o terms.txt terms.txt")
	terms = open("terms.txt", "r").read()
	termKeys = re.findall(".+(?=:)", terms)
	termData = re.findall("(?<=:)[0-9]+", terms)
	sortedFile2 = open("sortedTerms.txt", "w")
	for i in range(len(termKeys)):
		sortedFile2.write(termKeys[i] + "\n")
		sortedFile2.write(termData[i] + "\n")
	sortedFile2.close()


	os.system("sort -u -o dates.txt dates.txt")
	dates = open("dates.txt", "r").read()
	dateKeys = re.findall(".+(?=:)", dates)
	dateData = re.findall("(?<=:)[0-9]+", dates)
	sortedFile3 = open("sortedDates.txt", "w")
	for i in range(len(dateKeys)):
		#print(i)
		sortedFile3.write(dateKeys[i] + "\n")
		sortedFile3.write(dateData[i] + "\n")
	sortedFile3.close()

def createIndex():
	os.system("db_load -f sortedTweets.txt -c duplicates=1 -T -t hash tw.idx")
	print("1st idx done")
	os.system("db_load -f sortedTerms.txt -c duplicates=1 -T -t btree te.idx")
	print("2nd idx done")	
	os.system("db_load -f sortedDates.txt -c duplicates=1 -T -t btree da.idx")
	print("3rd idx done")

main()
