import feedparser
from os import path
import warnings
import urllib3
import requests
import xml.etree.ElementTree as ET
import os

from bs4 import BeautifulSoup

warnings.simplefilter(action='ignore', category=FutureWarning)


if __name__ == '__main__':

    url = 'https://research.checkpoint.com/feed/'
    parsed_feed = feedparser.parse(url)

    # parsing xml to extract IOCS
    urllib3.disable_warnings()
    url = 'https://research.checkpoint.com/feed/'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)  # get
    # print(response.status_code)
    # print(response.text)

    # content = []
    # # Read the XML file
    # with open("feed.xml", "r") as file:
    #     # Read each line in the file, readlines() returns a list of lines
    #     content = file.readlines()
    #     # Combine the lines in the list into a string
    #     content = "".join(content)
    #     bs_content = BeautifulSoup(content, "lxml")
    #
    # result = bs_content.find("strong") #<strong>Top Attacks and Breaches</strong>
    # #result = bs_content.find_all("strong") # [<strong>Top Attacks </strong>...<strong>Top Attacks </strong>]
    # print(result)
    #
    # # h1_tag = bs_content.find_all("h1")
    # # result2 = h1_tag.contents
    # # print(result2)


    # getting [] None, None
    # # Parse XML from a file object
    # BeautifulSoup(markup, "lxml-xml")
    # with open("feed.xml") as file:
    #     soup = BeautifulSoup(file, features="lxml-xml")
    #
    # # Parse XML from a Python string
    # soup = BeautifulSoup("IOCs", features="lxml-xml")
    # print(soup.prettify())
    #
    # print(soup.find_all("<h1>IOCs</h1>", limit=10))
    # print(soup.find("<h1>IOCs</h1>"))
    # print(soup.find("IOCs"))



    # f = open("feed.xml", "x")
    # f.write(response.text)
    # with open('feed.xml') as f:
    #     lines = f.read()

    # print(lines)
    # mytree = ET.parse('feed.xml')
    # myroot = mytree.getroot()
    # print(mytree)
    # print(myroot)



# ---------------------------------------------

    links_list = []
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
                links_list.append(item.link)
                # print(item.link)
                # print(True)

            # elif "Indicator of compromise" in content.value:
            #     print(item.link)
            #     print(True)
    print(links_list)
    print("done")