import requests, lxml, json, time
import tldextract
from bs4 import BeautifulSoup

# Specify User Agent & cookie acceptance to bypass daft cookie signin/acceptance
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0"
}
cookies = {"CONSENT": "YES+cb.20220419-08-p0.cs+FX+111"}

listOfKeywords = ["loans", "grants", "taxes"]
numberOfTimes = 2
resultDict = {}

for keyword in listOfKeywords:
    companyList = []  # successful scrape added to list score ranking for absolute top and bottom
    numOfTopAds = 0
    numOfBottomAds = 0
    resultDict[keyword] = {}
    absolute_top = 0

    for _ in range(numberOfTimes):

        payload = {'q': keyword}
        html = requests.get("https://www.google.com/search?q=", params=payload, headers=headers, cookies=cookies)
        status_code = html.status_code

        # if status code met, the loop will continue for each keyword in the list
        if status_code == 200:

            response = html.text
            soup = BeautifulSoup(response, 'lxml')
            print('----------------Top Ads-------------------')

            topAds = soup.find(id='tvcap')
            if topAds:
                if len(topAds.findAll('div', class_='uEierd')) > 0:
                    numOfTopAds += 1
                absolute_top = 0
                for container in topAds.findAll('div', class_='uEierd'):
                    try:
                        advertisementTitle = container.find('div', class_='CCgQ5 vCa9Yd QfkTvb N8QANc Va3FIb EE3Upf').span.text
                    except AttributeError:
                        advertisementTitle = 'N/A'
                    try:
                        company = container.find('div', class_='d8lRkd').find('span', class_='x2VHCd OSrXXb ob9lvb').text
                        company = tldextract.extract(company).domain
                    except AttributeError:
                        company = 'N/A'
                    if company not in companyList:
                        companyList.append(company)
                        if absolute_top == 0:
                            resultDict[keyword][company] = {'absolute-top': 1, 'top': 0, 'bottom': 0}
                        else:
                            resultDict[keyword][company] = {'absolute-top': 0, 'top': 1, 'bottom': 0}
                    else:
                        if absolute_top == 0:
                            resultDict[keyword][company]['absolute-top'] += 1
                        else:
                            resultDict[keyword][company]['top'] += 1
                    try:
                        productDescription = container.find('div', class_='Va3FIb r025kc lVm3ye').text
                    except AttributeError:
                        productDescription = 'N/A'

                    print(company)
                    print(advertisementTitle)
                    print(productDescription)
                    absolute_top += 1
            time.sleep(4)
            print('----------------Bottom Ads-------------------')

            bottomads = soup.find(id='bottomads')
            if bottomads:
                if len(bottomads.findAll('div', class_='uEierd')) > 0:
                    numOfBottomAds += 1
                for container in bottomads.findAll('div', class_='uEierd'):
                    try:
                        advertisementTitle = container.find('div', class_='CCgQ5 vCa9Yd QfkTvb N8QANc Va3FIb EE3Upf').span.text
                    except AttributeError:
                        advertisementTitle = 'N/A'
                    try:
                        company = container.find('div', class_='d8lRkd').find('span', class_='x2VHCd OSrXXb ob9lvb').text
                        company = tldextract.extract(company).domain
                    except AttributeError:
                        company = 'N/A'
                    if company not in companyList:
                        companyList.append(company)
                        resultDict[keyword][company] = {'absolute-top': 0, 'top': 0, 'bottom': 1}
                    else:
                        resultDict[keyword][company]['bottom'] += 1
                    try:
                        productDescription = container.find('div', class_='Va3FIb r025kc lVm3ye').text
                    except AttributeError:
                        productDescription = 'N/A'

                    print(company)
                    print(advertisementTitle)
                    print(productDescription)
    keys = list(resultDict[keyword].keys())
    for name in ['bottom', 'top', 'absolute-top']:
        keys.sort(key=lambda k: resultDict[keyword][k][name], reverse=True)

    resultDict['total top ads'] = numOfTopAds
    resultDict['total bottom ads'] = numOfBottomAds

print(json.dumps(resultDict, indent=4))
