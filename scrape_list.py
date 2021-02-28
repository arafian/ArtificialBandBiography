from bs4 import BeautifulSoup
import requests
import sys
import re

try:
	url = sys.argv[1]
except:
	exit()

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

for a in soup.find_all("a", href=True):
	if a['href'][:6] == "/wiki/" and not ":" in a['href']:
		suburl = "https://en.wikipedia.org" + a['href']
		subresponse = requests.get(suburl)
		subsoup = BeautifulSoup(subresponse.content, "html.parser")
		first_sentence = subsoup.select("p")[0].getText().split(".")[0]
		if re.search(r'\bband\b', first_sentence) and not re.search(r'\balbum\b', first_sentence):
			print(suburl)
