import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import streamlit_tags as st_tags
import requests, lxml, json, time
import tldextract
from bs4 import BeautifulSoup

def displayScrapeResult():
    st.write('display results')

def googleAdScraper(numberOfScrape,selected_keywords):

    st.subheader('Progress:')
    my_bar = st.progress(0)
    # Specify User Agent & cookie acceptance to bypass daft cookie signin/acceptance
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0"
    }
    cookies = {"CONSENT": "YES+cb.20220419-08-p0.cs+FX+111"}
    resultDict = {}
    progress=0

    for keyword in selected_keywords:
        companyList = []  # successful scrape added to list score ranking for absolute top and bottom
        numOfTopAds = 0
        numOfBottomAds = 0
        resultDict[keyword] = {}
        absolute_top = 0

        for _ in range(numberOfScrape):

            payload = {'q': keyword}
            html = requests.get("https://www.google.com/search?q=", params=payload, headers=headers, cookies=cookies)
            status_code = html.status_code

            # if status code met, the loop will continue for each keyword in the list
            if status_code == 200:

                response = html.text
                soup = BeautifulSoup(response, 'lxml')
                #top ads
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
                    progress += (0.5/len(selected_keywords)*numberOfScrape)
                    my_bar.progress(progress)
                time.sleep(4)
                
                #bottom ads
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
                    progress += (0.5/len(selected_keywords)*numberOfScrape)
                    my_bar.progress(progress)
        keys = list(resultDict[keyword].keys())
        for name in ['bottom', 'top', 'absolute-top']:
            keys.sort(key=lambda k: resultDict[keyword][k][name], reverse=True)

        resultDict['total top ads'] = numOfTopAds
        resultDict['total bottom ads'] = numOfBottomAds
    print(json.dumps(resultDict, indent=4))
    st.success('"Google Ads Scraping Complete!')
    return resultDict

def jsonToDataFrame(resultDict,selected_keywords):
    resultList = []
    for keyword in selected_keywords:
        if (resultDict[keyword]["top performers"] != []):
            for company in resultDict[keyword]["top performers"]:
                topPercentage = 0
                bottomPercentage = 0
                if resultDict[keyword]["total top ads"] != 0:
                    topPercentage = round((resultDict[keyword][company]["top"]+resultDict[keyword][company]["absolute-top"])/resultDict[keyword]["total top ads"] * 100,1)
                if resultDict[keyword]["total bottom ads"] != 0:
                    bottomPercentage = round(resultDict[keyword][company]["bottom"]/resultDict[keyword]["total bottom ads"] * 100,1)

                resultList.append(
                    [
                    keyword,
                    company,
                    resultDict[keyword][company]["absolute-top"],
                    resultDict[keyword][company]["top"],
                    resultDict[keyword][company]["bottom"],
                    topPercentage,
                    bottomPercentage,
                    round((resultDict[keyword]["total top ads"] + resultDict[keyword]["total bottom ads"])/(numberOfScrape*2) * 100,1),
                    ]
                )
        else:
            resultList.append([keyword,None,0,0,0,0,0,0])

    df = pd.DataFrame(resultList,columns=["Keyword","Company","absolute-top","top","bottom","top(%)","bottom(%)","Keyword Ads Percentage(%)"])
    return df
st.title("Add People: Keyword Analysis Dashobard")

numberOfScrape = st.slider("How many  times do  you wnat the keyword scraper to be ran?",1,5,1)
listOfKeywords = ["plumber","builder","accountant"]

col1,col2= st.columns(2)
with col1:
    selected_keywords = st_tags(
        label="Add Keyword!",
        text="Press Enter To Adde Another Keyword",
        value=listOfKeywords,
        suggestions=['accountancy','loans','electrician'],
        maxtags=8,
        key='aljnf'
    )
with col2:
    st.caption("Current KeyWord List")

submitted = st.button("Submit")

if submitted:
    st.write("Scraping google for the selcted keywords:",str(selected_keywords),'for',numberOfScrape, ' times!')
    st.write("Submission Complte")

    resultDict = googleAdScraper(numberOfScrape,selected_keywords)
    rawDataOutput = jsonToDataFrame(resultDict,selected_keywords)
    result_df = st.dataframe(rawDataOutput)

displayResult = st.button("Display Result")
if displayResult:
    displayScrapeResult()
