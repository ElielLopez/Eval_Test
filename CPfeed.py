import feedparser
from os import path
import warnings
import urllib3
import requests
import datetime
import iocextract
import bs4
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


# ---------------------------------------------

    links_list = []
    # create file for IOCs if not exist, if does exist, append IOCs tot he end of the file.
    if not path.exists("IOCs.txt"):
        f = open("IOCs.txt", "x")
        f.write(datetime.datetime.now().ctime())
        f.write("\n")
    else:
        f = open("IOCs.txt", "a")
        f.write('\n')
        f.write(datetime.datetime.now().ctime())
        f.write('\n')

    for item in parsed_feed.entries:
        # print(item.title)
        # print(item.published)
        # print(item.link)
        for content in item.content:
            # if IOC found in article, write the link into the IOCs file
            if "IOC" in content.value:
                # f = open("IOCs.txt", "a")
                f.write(item.link)
                f.write('\n')
                links_list.append(item.link)
                # print(item.link)
                # print(True)

            elif "Indicators of Compromise" in content.value:
                f.write(item.link)
                f.write('\n')
                links_list.append(item.link)

    list_size = len(links_list)
    print("the size of the list is: ", list_size)

    for i in range(0, list_size):

        parsed_feed = feedparser.parse(links_list[i])
        urllib3.disable_warnings()
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(links_list[i], headers=headers)  # get
        # print(response.status_code)
        # print(response.text)

        doc = bs4.BeautifulSoup(response.content, 'html.parser')
        for ioc in iocextract.extract_iocs(doc.get_text(separator=' '), refang=True, strip=True):
            print(ioc.encode('utf-8'))
        print("-------------------------------------------\n")


    print("done")