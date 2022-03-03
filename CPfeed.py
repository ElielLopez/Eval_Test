import flask
import requests
import urllib3
import feedparser
import re
from bs4 import BeautifulSoup
import requests
import pandas
from requests_html import HTML
from requests_html import HTMLSession
import os.path
from os import path
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# urllib3.disable_warnings()
# url = 'https://research.checkpoint.com/feed/'
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
# response = requests.post(url, headers=headers)  # get
# print(response.status_code)
# print(response.text)
# print(response.content)


# get feed function received url of rss feed and return the feed content
# def get_feed(url):
#     response = get_source(url)
#     data_frame = pandas.DataFrame(columns=['title', 'pubDate', 'guid', 'description'])
#
#     with response as r:
#         items = r.html.find("item", first=False)
#
#         for item in items:
#             title = item.find('title', first=True).text
#             pubDate = item.find('pubDate', first=True).text
#             guid = item.find('guid', first=True).text
#             description = item.find('description', first=True).text
#
#             row = {'title': title, 'pubDate': pubDate, 'guid': guid, 'description': description}
#             data_frame = data_frame.append(row, ignore_index=True)
#
#     return data_frame
#
#
# # get source receives url to rss feed and return the source code (http)
# def get_source(url):
#     try:
#         session = HTMLSession()
#         response = session.get(url)
#         return response
#
#     except requests.exceptions.RequestException as e:
#         print(e)


if __name__ == '__main__':
    # url = "https://research.checkpoint.com/feed/"
    # d_frame = get_feed(url)
    # d_frame.head()
    # print(d_frame)

    # NewFeed = feedparser.parse("https://research.checkpoint.com/feed/")
    # # returns how many articles in the feed.
    # num_of_articles = len(NewFeed.entries)
    # print("Number of recent publication: ", num_of_articles)
    # # getting lists of article entries
    # articles = NewFeed.entries
    #
    # # dictionary for holding articles details
    # # articles_details = {"article title": NewFeed.feed.title, "article link": NewFeed.feed.link}
    # article_list = []
    #
    # # print(NewFeed.feed)
    #
    # # iterating over individual posts
    # for article in articles:
    #     temp = dict()
    #
    #     # if any post doesn't have information then throw error.
    #     try:
    #         temp["title"] = article.title
    #         temp["author"] = article.author
    #         temp["time_published"] = article.published
    #         temp_summary = article.summary
    #         # sentences = temp_summary.split('<p> <a href= </a>')
    #         sentences = re.split("<p>", temp_summary)
    #         temp["summary"] = sentences
    #     except:
    #         pass
    #
    #     article_list.append(temp)
    #
    # for a in article_list:
    #     print(a["time_published"], a["title"], a["author"], "\n")
    url = 'https://research.checkpoint.com/feed/'
    parsed_feed = feedparser.parse(url)

    # create file for IOCs if not exist, if does exist, append IOCs tot he end of the file.
    if not path.exists("IOCs.txt"):
        f = open("IOCs.txt", "x")
    else:
        f = open("IOCs.txt", "a")
        f.write('\n')

    for item in parsed_feed.entries:
        print(item.title)
        print(item.published)
        for content in item.content:
            # if IOC found in article, write the link into the IOCs file
            if "IOC" in content.value:
                # f = open("IOCs.txt", "a")
                f.write(item.link)
                f.write('\n')
                print(item.link)
                print(True)

            # elif "Indicator of compromise" in content.value:
            #     print(item.link)
            #     print(True)
    print("done")