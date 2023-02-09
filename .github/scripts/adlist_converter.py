import re
import os
import argparse 
import urllib3
import requests

def arg_parse():
	''' Argparser.
	'''
	parser = argparse.ArgumentParser(description='Convert AdBlock list to text')
	URL = parser.add_argument(
		'url',
		type=str,
		help='input url')
	local_args = parser.parse_args()
	return local_args

def cleanCSV(bList):
	''' Clean CSVs.
		- remove domains with *
	'''
	aList = []
	for item in bList.split(","):
		if not("*" in item):
			aList.append(item)
	return aList

def checkCSV(string):
	''' Check string for CSV.
		- looks for ##, #@# and #
	'''
	s = False
	for n in range(0, len(string)):
		if string[n] == "*":
			s = True
		if string[n] == "#":
			if s == False:
				return string[:n].split(",")
			if s == True: 
				return cleanCSV(string[:n])

def cleanAdstr(string):
	'''	Get domain from string.
		- excludes: wildcards, incomplete domains
	'''
	for n in range(0, len(string)):
		if string[n] == ("*" or ".js" or "/" or "~"):
			break
		if string[n] == "^":
			return string[:n]
		if string[n] == "$":
			break

def getFilename(inURL):
	''' Get filename from URL.
		- first "/" from right
	'''
	for n in range(0, len(inURL)):
		if inURL[-n] == "/":
			return inURL[len(inURL)-n+1:]

def getAdList(inURL):
	''' Get raw blocklist text file.
	'''
	requests.packages.urllib3.disable_warnings()
	res = requests.get(inURL)
	if not ("text/plain" in res.headers['content-type']):	#  check content type is plain text
		raise Exception("Content Type: ", res.headers['content-type'], " does not match text/plain.")
	if res.status_code != 200:	#  check OK response
		raise Exception("Status Code: ",res.status_code," Error: ",res.text)
	if res.text == None:	# check for data
		raise Exception("No data in response. ",res.headers, res.text)
	return res.text

def writeList(inURL, adList, newFile):
	''' Create parsed blocklist file.
	'''
	csvStack = []
	writer = open(newFile, 'w')
	writer.write("# Converted by: https://github.com/anthonytwh/pihole-blocklist-converter"+"\n")
	writer.write("# Blocklist: "+inURL+"\n")
	for line in adList.splitlines():
		if line:
			try:
				if line.startswith(("#", "!", "/", "|", "-", "@", "*", "^", "$")) == False:
					lineList = checkCSV(line)
					if (lineList) and (lineList != csvStack):
						writer.writelines("\n".join(lineList)+"\n")
					csvStack = lineList 	# don't write duplicate lists
			except:
				pass

			try: 
				if line.startswith("@@||") == True:
					line = cleanAdstr(line[4:])
					if line:
						writer.write(line+"\n")
			except: 
				pass

			try: 
				if line.startswith("||") == True:
					line = cleanAdstr(line[2:])
					if line:
						writer.write(line+"\n")
			except: 
				pass

def main():
  urls = ["https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/annoyances.txt",
          "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/badware.txt",
          "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters-2020.txt",
          "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters-2021.txt",
          "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters-2022.txt",
          "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters-2023.txt",
          "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters.txt",
          "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/privacy.txt",
          "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/resource-abuse.txt",
          "https://easylist.to/easylist/easylist.txt",
          "https://easylist.to/easylist/easyprivacy.txt"]
  for i in range(10):
    inURL = urls[i]
    adList = getAdList(inURL)
    fileName = getFilename(inURL)
    newFile = "external/" + fileName
    writeList(inURL, adList, newFile)
    
main()
