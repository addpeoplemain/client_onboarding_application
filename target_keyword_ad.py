import requests, lxml, json, time
import tldextract
from bs4 import BeautifulSoup

# Specify User Agent 

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0"
}
cookies = {"CONSENT": "YES+cb.20220419-08-p0.cs+FX+111"}
listOfKeywords = ["nft","crypto","bitcoin"]
numberOfTimes = 3
resultDict = {}

payload = {'q': listOfKeywords[0]}
html = requests.get("https://www.google.com/search?q=",params=payload,headers=headers,cookies=cookies)

response = html.text
soup = BeautifulSoup(response,'lxml')
print(soup)
   
with open("output.html","w", encoding="utf-8") as file:
  file.write(str(soup))

 