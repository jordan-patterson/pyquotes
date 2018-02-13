#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import os
import json
from random import choice

home = os.path.expanduser("~")
directory = home+"/bin/pyquotes/"

def initialize():
	types=getTypes()
	categories=[]
	for t in types:
		categories.append(getCategories(t))
	links={"categories":categories}
	if(not os.path.exists(directory)):
		os.makedirs(directory)
	with open(directory+"links.json","w") as file:
		json.dump(links,file)
	return links

def getTypes():
	types=[]
	r = requests.get("https://quotefancy.com")
	if r.status_code==200:
		soup=BeautifulSoup(r.text,markup="html")
		links = soup.find_all('a')
		for a in links:
			link=a.get('href')
			temp="quotes"
			if(link not in types):
				if(link):
					if(temp in link):
						types.append(link)
	return types

def getCategories(link):
	categories=[]
	r = requests.get(link)
	if r.status_code==200:
		soup=BeautifulSoup(r.text,markup="html")
		links=soup.find_all('a')
		for a in links:
			link=a.get('href')
			temp="quotes"
			if(link not in categories):
				if(link):
					if(temp in link):
						categories.append(link)
	return categories


def getQuotes(link):
	links = []
	r = requests.get(link)
	if r.status_code==200:
		print("successful")
		soup = BeautifulSoup(r.text)
		quotes = soup.find_all('a')
		for i in quotes:
			link = i.get('href')
			temp="quote/"
			if(link not in links):
				if(link):
					if(temp in link):
						links.append(link)
	return links

def getImages(link):
	links=[]
	r = requests.get(link)
	if r.status_code==200:
		soup=BeautifulSoup(r.text)
		images = soup.find_all('img')
		for i in images:
			source = i.get('data-original')
			temp="wallpaper/1600x900"
			if(source not in links):
				if(source):
					if(temp in source):
						links.append(source)
	return links

def getImage(link):
	chunk_size=1024
	filename=link.split('/')[-1]
	r = requests.get(link,stream=True)
	with open(filename,"wb") as file:
		for chunk in r.iter_content(chunk_size=chunk_size):
			file.write(chunk)
	os.system("xdg-open '"+filename+"'")

def main():
	if(not os.path.exists(directory+"links.json")):
		links=initialize()
	else:
		with open(directory+"links.json","r") as file:
			links = json.load(file)
	categories=links["categories"]
	category=choice(categories)
	#print(category)
	link = choice(category)
	print(link)
	quotes = getQuotes(link)
	#print(quotes)
	quote = choice(quotes)
	#print(quote)
	images=getImages(quote)
	#print(images)
	image=choice(images)
	getImage(image)

if __name__=="__main__":
	main()