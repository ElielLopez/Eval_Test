import feedparser
from os import path
import warnings
import urllib3
import requests
import datetime
import iocextract
import bs4
import csv
import regex
from bs4 import BeautifulSoup

warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__ == '__main__':
    # the desired url to parse
    url = 'https://research.checkpoint.com/feed/'
    parsed_feed = feedparser.parse(url)

    # passing 403 forbidden warning
    urllib3.disable_warnings()
    url = 'https://research.checkpoint.com/feed/'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)  # get
    # creating containers for the CSV file data
    links_list = []
    title_list = []
    date_list = []

    # create file for IOCs links if not exist, if does exist, append IOCs tot he end of the file.
    # this file will help for deeper investigation if needed
    if not path.exists("IOCs_Links.txt"):
        f = open("IOCs_Links.txt", "x")
        f.write(datetime.datetime.now().ctime())
        f.write("\n")
    else:
        f = open("IOCs_Links.txt", "a")
        f.write('\n')
        f.write(datetime.datetime.now().ctime())
        f.write('\n')

    for item in parsed_feed.entries:
        # printing to terminal the desired data
        print(item.published)
        print(item.title)
        print(item.author)

        # create file for publications if not exist, if does exist
        if not path.exists("Publications_Summary.txt"):
            f2 = open("Publications_Summary.txt", "x")
        else:
            f2 = open("Publications_Summary.txt", "a")

        # writing the desired data to the created file- publications_summary
        f2.write(item.published)
        f2.write(',  "')
        f2.write(item.title)
        f2.write('",  published by: ')
        f2.write(item.author)
        f2.write("\n")

        for content in item.content:
            # if IOC\IOCs or Indicators of compromised found in article, write the link into the IOCs link file
            if "IOC" in content.value:
                # f = open("IOCs.txt", "a")
                f.write(item.link)
                f.write('\n')
                # appending to each container the corresponding data for CSV file
                links_list.append(item.link)
                title_list.append(item.title)
                date_list.append(item.published)

            elif "Indicators of Compromise" in content.value:
                f.write(item.link)
                f.write('\n')
                links_list.append(item.link)

    list_size = len(links_list)
    # creating CSV file with required headers
    csv_headers = ['Date', 'Title', 'IOC_Type', 'IOC']
    f = open('IOC_csv_file.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(csv_headers)

    for i in range(0, list_size - 1):
        parsed_feed = feedparser.parse(links_list[i])
        urllib3.disable_warnings()
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(links_list[i], headers=headers)  # get request
        doc = bs4.BeautifulSoup(response.content, 'html.parser')
        # helper variables
        temp_title = title_list[i]
        temp_date = date_list[i]
        # using ioc extract lib, extracting all indicators from each link
        # refang help to transfer ip\url such as 1[.]1[.]1[.]1 to 1.1.1.1 or [.]com to .com
        for ioc in iocextract.extract_iocs(doc.get_text(separator=' '), refang=True, strip=True):
            print(ioc.encode('utf-8')) # if want to print straight to terminal
            temp_size = len(ioc)
            # for sha256 indicator
            if temp_size == 64 and "http" not in ioc:
                temp_row = [temp_date, temp_title, 'SHA256', ioc]
                writer.writerow(temp_row)
            # for sha1 indicator
            elif temp_size == 40 and "http" not in ioc:
                temp_row = [temp_date, temp_title, 'SHA1', ioc]
                writer.writerow(temp_row)
            # for MD5 indicator
            elif temp_size == 32 and "http" not in ioc:
                temp_row = [temp_date, temp_title, 'MD5', ioc]
                writer.writerow(temp_row)
            # for url indicator
            elif "http" in ioc:
                temp_row = [temp_date, temp_title, 'URL', ioc]
                writer.writerow(temp_row)
            # for IP indicator
            else:
                temp_row = [temp_date, temp_title, 'IP', ioc]
                writer.writerow(temp_row)

    print("done")
