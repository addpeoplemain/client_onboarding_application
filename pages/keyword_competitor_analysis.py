import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from streamlit_tags import st_tags
import requests, lxml, json, time
import tldextract
from bs4 import BeautifulSoup

def displayScrapeResult():
    st.write('display results')
    st.title(':bar_chart: Data visualisation')
    df = pd.read_csv('GoogleAdScraperResult.csv')

    keywords = df['Keyword'].unique().tolist()
    keyword_selection = st.multiselect('Keyword:',keywords,default=keywords)
    if not keyword_selection:
        st.error("Please select at least one keyword to display the dataframe.")
    mask = df['Keyword'].isin(keyword_selection)
    number_of_result = df[mask].shape[0]
    st.markdown(f'*Available rows: {number_of_result}*')
    st.dataframe(df[mask])

    # st.dataframe(groupedKeywordPercentage_df)
    groupedKeywordPercentage_df = generateKeywordAdPercentage(df)
    # remove rows with zero percentage
    groupedKeywordPercentage_df = groupedKeywordPercentage_df[groupedKeywordPercentage_df.Percentage != 0]


    # plot bar chart
    bar_chart = px.bar(
        groupedKeywordPercentage_df,
        x="Keyword",
        y="Percentage",
        text="Percentage",
        template="plotly_white",
        title="Keyword Ads Percentage(%)"
    )
    st.plotly_chart(bar_chart)
# Generate Keyword Ads Appearance Percentage
def generateKeywordAdPercentage(df):
    keywordAdPercentage = []
    for keyword in df['Keyword'].unique().tolist():
        if df[df['Keyword'] == keyword]['Keyword Ads Percentage(%)'].max() is None:
            keywordAdPercentage.append(0)
        else:
            keywordAdPercentage.append(df[df['Keyword'] == keyword]['Keyword Ads Percentage(%)'].max())

    groupedKeywordPercentage_df = pd.DataFrame(list(zip(df['Keyword'].unique().tolist(), keywordAdPercentage)),columns =['Keyword', 'Percentage'])
    groupedKeywordPercentage_df = groupedKeywordPercentage_df.sort_values(by=['Percentage'],ascending=False)
    return groupedKeywordPercentage_df
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
                    if progress >= 1:
                        my_bar.progress(1)
                    else:
                        my_bar.progress(0)
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
                    if progress >= 1:
                        my_bar.progress(1)
                    else:
                        my_bar.progress(0)
        keys = list(resultDict[keyword].keys())
        for name in ['bottom', 'top', 'absolute-top']:
            keys.sort(key=lambda k: resultDict[keyword][k][name], reverse=True)
        resultDict[keyword]['top performers'] = keys
        resultDict[keyword]['total top ads'] = numOfTopAds
        resultDict[keyword]['total bottom ads'] = numOfBottomAds
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
st.title("Add People: Keyword Competitor Analysis Dashboard")

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color:#F7F5F2 ;
        color: #173340;
        
    }
  

</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("logo.png")
    st.write("""
                 
         **Onboarding Application 1.0**
         
         Onboarding Application 1.0
                 
        

            """
         )

numberOfScrape = st.slider("How many  times do  you want the keyword scraper to be ran?",1,5,1)
listOfKeywords = ["plumber","builder","accountant"]

col1,col2= st.columns(2)
with col1:
    selected_keywords = st_tags(
        label="Add Keyword!",
        text="Press Enter To Add Another Keyword",
        value=listOfKeywords,
        suggestions=['accountancy','loans','electrician'],
        maxtags=8,
        key='aljnf'
    )
with col2:
    st.caption("Current KeyWord List")
    st.write(selected_keywords)

submitted = st.button("Submit")

if submitted:
    st.write("Scraping google for the selcted keywords:",str(selected_keywords),'for',numberOfScrape, ' times!')
    st.write("Submission Complte")

    resultDict = googleAdScraper(numberOfScrape,selected_keywords)
    rawDataOutput = jsonToDataFrame(resultDict,selected_keywords)
    result_df = st.dataframe(rawDataOutput)
    rawDataOutput.to_csv('GoogleAdScraperResult.csv',index=False)

displayResult = st.button("Display Result")
if displayResult:
    displayScrapeResult()
