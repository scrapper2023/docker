# import Hindustan_Times as HT
# import timesnow as TN
# import TOI_Final as TOI
# import Indiatoday as IT
# import Republic as Rep
# import ndtv 
import ssl
import streamlit.components.v1 as components
import streamlit as st
import pickle
import plotly.express as px
from pathlib import Path
import streamlit_authenticator as stauth
import bcrypt
import plotly.express as px
import pytz
import urllib.request
import pandas as pd
import re
import os
import requests
import xml.etree.ElementTree as ET
import feedparser
from tqdm import tqdm
from datetime import datetime
import openpyxl
from dateutil.parser import parse as parse_date
from newspaper import Config, Article

def fetch_articles(rss_url, num_pages):
    # Create an empty list to store the extracted data
    data = []

    # Iterate over the specified number of pages
    for page in range(1, num_pages + 1):
        # Append page number to the RSS feed URL
        page_url = f"{rss_url}?page={page}"

        # Parse the RSS feed
        feed = feedparser.parse(page_url)

        # Extract relevant information from each entry in the feed
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            published = entry.published

            # Convert the publication date to a datetime object
            if rss_url == 'https://www.republicworld.com/rss/world-news.xml':
                pub_date_utc = datetime.strptime(
                    published, "%a, %d %b %Y %H:%M:%S %Z")
                utc_tz = pytz.timezone('GMT')
                ist_tz = pytz.timezone('Asia/Kolkata')
                pub_date_utc = utc_tz.localize(pub_date_utc)
                pub_date_ist = pub_date_utc.astimezone(ist_tz)
                published = pub_date_ist.strftime("%Y-%m-%d %H:%M:%S")
            else:
                pub_date = parse_date(published)
                published = pub_date.strftime("%Y-%m-%d %H:%M:%S")

            # Add the extracted data to the list
            data.append({
                'Source': rss_url,
                'Title': title,
                'Link': link,
                'Published': published
            })

    return data



# Function to combine articles from multiple sources
def ndtv():
    # Fetch articles from each source
    articles_data = []
    for source, rss_url in rss_urls.items():
        articles = fetch_articles(rss_url,1)
        articles_data.extend(articles)

    # Create a DataFrame from the fetched data
    articles_df = pd.DataFrame(articles_data)
    articles_df.drop_duplicates(subset=['Link'], inplace=True)
    return articles_df


# Function to save DataFrame to Excel file
# def save_to_excel(df, filename):
#     # Create a Pandas Excel writer using openpyxl engine
#     writer = pd.ExcelWriter(filename, engine='openpyxl')

#     # Write the DataFrame to the Excel file
#     df.to_excel(writer, index=False)

#     # Save the Excel file
#     writer.close()

#     print(f"Data saved to {filename}.")


# RSS feed URLs and number of pages to retrieve
rss_urls = {


    'NDTV World News': 'https://feeds.feedburner.com/ndtvnews-world-news',
    'NDTV India News': 'https://feeds.feedburner.com/ndtvnews-india-news',
    'NDTV Top Stories': 'https://feeds.feedburner.com/ndtvnews-top-stories',
    'NDTV Trending News': 'https://feeds.feedburner.com/ndtvnews-trending-news',
    'NDTV Movies': 'https://feeds.feedburner.com/ndtvmovies-latest',
    'NDTV Profit': 'https://feeds.feedburner.com/ndtvprofit-latest',
    'NDTV Latest News': 'https://feeds.feedburner.com/ndtvnews-latest',
    'NDTV Sports': 'https://feeds.feedburner.com/ndtvsports-latest',
    'NDTV Gadgets': 'https://feeds.feedburner.com/gadgets360-latest',
    'NDTV Cars and Bikes': 'https://feeds.feedburner.com/carandbike-latest',
    'NDTV Cricket': 'https://feeds.feedburner.com/ndtvsports-cricket',
    'NDTV Cities News': 'https://feeds.feedburner.com/ndtvnews-cities-news',
    'NDTV South India News': 'https://feeds.feedburner.com/ndtvnews-south',
    'NDTV Indians Abroad': 'https://feeds.feedburner.com/ndtvnews-indians-abroad',
    'NDTV Cooks': 'https://feeds.feedburner.com/ndtvcooks-latest',
    'NDTV Offbeat News': 'https://feeds.feedburner.com/ndtvnews-offbeat-news',
    'NDTV People': 'https://feeds.feedburner.com/ndtvnews-people',
    'NDTV Latest Videos': 'https://feeds.feedburner.com/ndtv/latest-videos',

}




def fetch_articles(rss_url, num_pages):
    # Create an empty list to store the extracted data
    data = []

    # Iterate over the specified number of pages
    for page in range(1, num_pages + 1):
        # Append page number to the RSS feed URL
        page_url = f"{rss_url}?page={page}"

        # Parse the RSS feed
        feed = feedparser.parse(page_url)

        # Extract relevant information from each entry in the feed
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            published = entry.published

            # Convert the publication date to a datetime object
            if rss_url == 'https://www.republicworld.com/rss/world-news.xml':
                pub_date_utc = datetime.strptime(
                    published, "%a, %d %b %Y %H:%M:%S %Z")
                utc_tz = pytz.timezone('GMT')
                ist_tz = pytz.timezone('Asia/Kolkata')
                pub_date_utc = utc_tz.localize(pub_date_utc)
                pub_date_ist = pub_date_utc.astimezone(ist_tz)
                published = pub_date_ist.strftime("%Y-%m-%d %H:%M:%S")
            else:
                pub_date = parse_date(published)
                published = pub_date.strftime("%Y-%m-%d %H:%M:%S")

            # Add the extracted data to the list
            data.append({
                'Source': rss_url,
                'Title': title,
                'Link': link,
                'Published': published
            })

    return data


# Function to combine articles from multiple sources
def republic():
    # Fetch articles from each source
    articles_data = []
    rss_urls = {

        'Republic World': 'https://www.republicworld.com/rss/world-news.xml',
        'Republic World: India News': 'https://www.republicworld.com/rss/india-news.xml',
        'Republic World: Sports News': 'https://www.republicworld.com/rss/sports-news.xml',
        'Republic World: Entertainment News': 'https://www.republicworld.com/rss/entertainment-news.xml',
        'Republic World: Technology News': 'https://www.republicworld.com/rss/technology-news.xml',
        'Republic World: Business News': 'https://www.republicworld.com/rss/business-news.xml',


    }

    num_pages = 25
    for source, rss_url in rss_urls.items():
        articles = fetch_articles(rss_url, num_pages)
        articles_data.extend(articles)

    # Create a DataFrame from the fetched data
    articles_df = pd.DataFrame(articles_data)
    articles_df.drop_duplicates(subset=['Link'], inplace=True)
    return articles_df




def India_Today():
    urls = {
        'India Today 1': 'https://www.indiatoday.in/rss/home',
        'India Today 2': 'https://www.indiatoday.in/rss/1206514',
        'India Today 3': 'https://www.indiatoday.in/rss/1206614',
        'India Today 4': 'https://www.indiatoday.in/rss/1206494',
        'India Today 5': 'https://www.indiatoday.in/rss/1206577',
        'India Today 6': 'https://www.indiatoday.in/rss/1206500',
        'India Today 7': 'https://www.indiatoday.in/rss/1206550',
        'India Today 8': 'https://www.indiatoday.in/rss/1206551',
        'India Today 9': 'https://www.indiatoday.in/rss/1206509',
        'India Today 10': 'https://www.indiatoday.in/rss/1206610',
        'India Today 11': 'https://www.indiatoday.in/rss/1206584',
        'India Today 12': 'https://www.indiatoday.in/rss/1206613',
        'India Today 13': 'https://www.indiatoday.in/rss/1206513',
        'India Today 14': 'https://www.indiatoday.in/rss/1206503',
        'India Today 15': 'https://www.indiatoday.in/rss/1206504'
    }

    # Create empty lists to store the data
    titles = []
    links = []
    published_datetimes = []

    # Iterate over each URL and extract the data
    for name, url in urls.items():
        # Parse the RSS feed
        feed = feedparser.parse(url)

        # Extract title, link, and published date time for each entry
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            published_datetime = entry.published

            titles.append(title)
            links.append(link)
            published_datetimes.append(published_datetime)

    # Create a dataframe
    data = {
        'Source':"India Today",
        'Title': titles,
        'Link': links,
        'Published': published_datetimes
    }
    df = pd.DataFrame(data)
    df.drop_duplicates(subset=['Link'], inplace=True)
    return df



# Define the news sources and their RSS feed URLs
news_sources = {
    '1Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms',
    '2Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/7098551.cms',
    '3Times of India': 'https://timesofindia.indiatimes.com/rssfeeds_us/72258322.cms',
    '4Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/54829575.cms',
    '5Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/4719148.cms',
    '6Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/-2128672765.cms',
    '7Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/2647163.cms',
    '8Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/66949542.cms',
    '9Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/913168846.cms',
    '10Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/1081479906.cms',
    '11Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/2886704.cms',
    '12Times of India': 'https://timesofindia.indiatimes.com/rssfeedmostread.cms',
    '13Times of India': 'https://timesofindia.indiatimes.com/rssfeedmostshared.cms',
    '14Times of India': 'https://timesofindia.indiatimes.com/rssfeedmostcommented.cms',
    '15Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/74317216.cms',
    '16Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/-2128838597.cms',
    '17Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/-2128839596.cms',
    '18Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/-2128833038.cms',
    '19Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/-2128816011.cms',
    '20Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/30359486.cms',
    '21Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/7098551.cms',
    '22Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/30359534.cms',
    '23Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/3907412.cms',
    '24Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/2177298.cms',
    '25Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/1898272.cms',
    '26Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/671314.cms',
    '27Times of India': 'https://timesofindia.indiatimes.com/rssfeedsvideo/3812907.cms',
    '28Times of India': 'https://timesofindia.indiatimes.com/rssfeedsvideo/3812908.cms',
    '29Times of India': 'https://timesofindia.indiatimes.com/rssfeedsvideo/3813456.cms',
    '30Times of India': 'https://timesofindia.indiatimes.com/rssfeedsvideo/3813443.cms',
    '31Times of India': 'https://timesofindia.indiatimes.com/rssfeedsvideo/3813458.cms',
    '32Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/2950623.cms',
    '33Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/-2128821153.cms',
    '34Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/3947060.cms',
    '35Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/4118235.cms',
    '36Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/7503091.cms',
    '37Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/6547154.cms',
    '38Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/4118215.cms',
    '39Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/3942695.cms',
    '40Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/3947067.cms',
    '41Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/-2128830821.cms',
    '42Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/3947051.cms',
    '43Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/3942690.cms',
    '44Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/3942693.cms',
    '45Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/8021716.cms',
    '46Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/-2128821991.cms',
    '47Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/3012535.cms',
    '48Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/-2128816762.cms',
    '49Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/-2128819658.cms',
    '50Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/-2128817995.cms',
    '51Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/3012544.cms',
    '52Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/442002.cms',
    '53Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/3942663.cms',
    '54Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/4118245.cms',
    '55Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/3942660.cms',
    '56Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/3942666.cms',
    '57Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/3947071.cms',
    '58Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/3831863.cms',
    '59Times of India': 'https://timesofindia.indiatimes.com/rssfeeds/878156304.cms',
}

# Function to fetch news data from a source


def fetch_news_data(url, num_pages):
    news_data = []

    for page in range(1, num_pages + 1):
        try:
            feed = feedparser.parse(f"{url}?page={page}")

            for entry in feed.entries:
                title = entry.title
                # author = entry.author if 'author' in entry else None
                published = entry.published_parsed if 'published_parsed' in entry else None
                # summary = entry.summary
                link = entry.link

                # Convert published time to a readable format
                if published:
                    published = datetime.fromtimestamp(
                        datetime(*published[:6]).timestamp()
                    ).strftime("%Y-%m-%d %H:%M:%S")

                news_item = {
                    'Source': 'Times of India',
                    'Title': title,
                    'Published': published,
                    'Link': link
                }

                news_data.append(news_item)
        except Exception as e:
            print(f"Error occurred while fetching data from {url}: {str(e)}")

    return news_data


    # Set the number of pages to fetch


def TOI():
    # Create an empty list to store the news data
    all_news_data = []
    num_pages = 14

    # Retrieve news data from each source
    for source, url in tqdm(news_sources.items(), desc='Fetching News'):
        news_data = fetch_news_data(url, num_pages)
        for item in news_data:
            item['Source'] = source
        all_news_data.extend(news_data)

    # Create a DataFrame from the news data
    df = pd.DataFrame(all_news_data)
    df.drop_duplicates(subset=['Link'], inplace=True)
    return df



def Times_Now():
    xml_link = "https://www.timesnownews.com/google-news-sitemap-en.xml"

    # Fetch the XML content from the link
    response = requests.get(xml_link)
    xml_content = response.content

    # Parse the XML content
    root = ET.fromstring(xml_content)
    # Define the XML namespace used in the document
    namespace = {
        "sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "news": "http://www.google.com/schemas/sitemap-news/0.9",
    }

    # Extract the title, link, and date
    articles = []
    for item in root.findall("sitemap:url", namespace):
        article = {}

        loc = item.find("sitemap:loc", namespace)
        if loc is not None and loc.text:
            article['link'] = loc.text

        title = item.find("news:news/news:title", namespace)
        if title is not None and title.text:
            article['title'] = title.text

        publication_date = item.find(
            "news:news/news:publication_date", namespace)
        if publication_date is not None and publication_date.text:
            article['date'] = publication_date.text

        articles.append(article)

    TN_data = []
    # Print the extracted data
    for article in articles:
        TN_data.append({
            'Source': "TimesNow News",
            'Title': article.get('title', 'N/A'),
            'Link': article.get('link', 'N/A'),
            'Published': article.get('date', 'N/A')
        })
    # Create a DataFrame from the dictionary
    df = pd.DataFrame(TN_data)
    df.drop_duplicates(subset=['Link'], inplace=True)
    return df

# print(len(Times_Now()))
def HT():
    xml_url = "https://www.hindustantimes.com/sitemap/news.xml"  # Replace with the actual XML URL

    # Fetch the XML data from the URL
    with urllib.request.urlopen(xml_url) as response:
        xml_data = response.read().decode('utf-8')

    # Now you can use the xml_data variable to work with the XML content
    print(xml_data)

    data = []

    xml_link="https://www.hindustantimes.com/sitemap/news.xml"

    # Extract HTML links and publishing times using regular expressions
    pattern = r"<loc>(https:\/\/www\.hindustantimes\.com\/.+?\.html)<\/loc>[\s\S]*?<news:publication_date>(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2})"
    matches = re.findall(pattern, xml_data)

    # Output the extracted links and publishing times
    for match in matches:
        link = match[0]
        time = match[1]
        pattern2="(https:\/(.)+\/)((.)+)(-(\d)+).html"
        matches2 = re.findall(pattern2, match[0])
        for matchh in matches2:
            title=matchh[2]
        data.append({"Source": "Hindustan Times", "Link": link, "Title":title, "Published": time})


    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)
    df.drop_duplicates(subset=['Link'], inplace=True)
    return df



# # Save the DataFrame to an Excel file
# save_dir = os.path.join(os.path.expanduser("~"), "Desktop")
# file_name = "HT.xlsx"
# output_file = os.path.join(save_dir, file_name)
# df.to_excel(output_file, index=False)


def final():
    try:
        # Your code that may raise an exception
        df=dashboard_page()
        return df  # Return the DataFrame if no exception occurs

    except Exception as e:
        # Handle the exception by returning a DataFrame with an error message
        error_df = pd.DataFrame({"Error": [f"An exception occurred: {e}"]})
        return error_df
    

def dashboard_page():
    HT_df = HT()
    Rep_df = republic()
    IT_df = India_Today()
    TN_df = Times_Now()
    ndtv_df = ndtv()
    TOI_df = TOI()

    # Function to save DataFrame to Excel file
    def save_to_excel(df, filename):
        # Create a Pandas Excel writer using openpyxl engine
        writer = pd.ExcelWriter(filename, engine='openpyxl')

        # Write the DataFrame to the Excel file
        df.to_excel(writer, index=False)

        # Save the Excel file
        writer.close()

        print(f"Data saved to {filename}.")

    combined_df_list = [TN_df, HT_df, Rep_df,IT_df, ndtv_df, TOI_df]

    def combine_articles(list_df):
        # Combine the dataframes
        combined_df = pd.concat(list_df, ignore_index=True)

        # Drop duplicate articles based on title and source
        combined_df.drop_duplicates(subset=['Link'], inplace=True)


        # Save the combined DataFrame to an Excel file
        # save_to_excel(combined_df, filename)

        return combined_df

    df=combine_articles(combined_df_list)
    y=len(TN_df)+len(HT_df)+ len(IT_df)+len(ndtv_df)+len(TOI_df)+ len(Rep_df)
    print(len(df), y)
    print("TN_df=",len(TN_df),' HT_df=',len(HT_df), " Republic_df=",len(Rep_df)," IndiaToday_df=",len(IT_df)," NDTV=",len(ndtv_df)," TOI_FP=",len(TOI_df))
    
    return df

names = ["Deependra","Yogita", "Lakshya", "nw18user"]
usernames = ["deependra","yogita", "lakshya","nw18user"]

file_path=Path(__file__).parent/"hashed_pw.pkl"

with file_path.open("rb") as file:
    hashed_passwords=pickle.load(file) 

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "news_scrapper", "abcdef", cookie_expiry_days=0)

name, authentication_status,username=authenticator.login("Login", "main")

if authentication_status ==False:
    st.error("Username/password is incorrect")

if authentication_status ==None:
    st.warning("Please enter username and password")

if authentication_status:
    authenticator.logout("Logout","sidebar")
    st.sidebar.title(f"Welcome {name}")
    ssl._create_default_https_context = ssl._create_unverified_context

            # Display "Hourglass and WAIT"
    # Custom CSS to center the spinner and make it larger
    spinner_css = """
        <style>
        .stSpinner>div {
            width: 100px !important;
            height: 100px !important;
            left: calc(50% - 50px);
            top: calc(50% - 50px);
        }
        </style>
    """

    # Display the spinner with custom CSS
    
    st.markdown(spinner_css, unsafe_allow_html=True)
    with st.spinner("Wait"):
        st.session_state['spinner_displayed'] = True  # Set the flag to indicate that the spinner is displayed

        # Load the data
        
        df=final()
        #converting df to csv file
        # Convert DataFrame to CSV bytes
        csv_data = df.to_csv(index=False).encode()
        # Get the current date and time
        # def get_current_time():
        #     ist = pytz.timezone('Asia/Kolkata')  # IST timezone
        #     current_time = datetime.datetime.now(ist)
        #     return current_time.strftime("%Y-%m-%d %H:%M:%S")
        current_datetime = datetime.now(pytz.timezone('Asia/Kolkata'))

    # Format the date and time as a string for the filename
        filename = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
        st.download_button('Download CSV', data=csv_data, file_name=f'{filename}.csv', mime='text/csv')
    # Redirect to the dashboard page
    #displaying the combined_df on dashboard page of streamlit
    st.title("News")
    # Display the DataFrame as a CSV table
    st.table(df)
 
    # #giving access to stored excel file for displaying on dashboard
    # combined_df = pd.read_excel('combined_articles_FP.xlsx')
    # #displaying the combined_df on dashboard page of streamlit
    # # st.dataframe(combined_df)
    # #download option for user and able to download the file
    # # #displaying the combined_df on dashboard page of streamlit
    # st.table(combined_df)
    # #displaying the combined_df on dashboard page of streamlit
    # st.write(combined_df)
    # #displaying the combined_df on dashboard page of streamlit
    # st.json(combined_df.to_json())
    # #displaying the combined_df on dashboard page of streamlit
    # st.code(combined_df)
    # #displaying the combined_df on dashboard page of streamlit
    # st.echo(combined_df)

    

