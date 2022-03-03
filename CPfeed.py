import feedparser
from os import path
import warnings
import urllib3
import requests
import datetime
import iocextract
import bs4
import csv
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
    title_list = []
    date_list = []
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
                title_list.append(item.title)
                date_list.append(item.published)
                # print(item.link)
                # print(True)

            elif "Indicators of Compromise" in content.value:
                f.write(item.link)
                f.write('\n')
                links_list.append(item.link)

    list_size = len(links_list)
    print("the size of the list is: ", list_size)

    csv_headers = ['Date', 'Title', 'IOC_Type', 'IOC']
    f = open('ioc_csv_file.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(csv_headers)
    for i in range(0, list_size - 1):

        parsed_feed = feedparser.parse(links_list[i])
        urllib3.disable_warnings()
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(links_list[i], headers=headers)  # get

        doc = bs4.BeautifulSoup(response.content, 'html.parser')

        temp_title = title_list[i]
        temp_date = date_list[i]
        for ioc in iocextract.extract_iocs(doc.get_text(separator=' '), refang=True, strip=True):

            # print(ioc.encode('utf-8'))

            temp_size = len(ioc)
            # if sha256
            if temp_size == 64 and "http" not in ioc:
                temp_row = [temp_date,temp_title,'SHA256',ioc]
                writer.writerow(temp_row)
            # if sha1
            elif temp_size == 40 and "http" not in ioc:
                temp_row = [temp_date,temp_title,'SHA1',ioc]
                writer.writerow(temp_row)
            # if MD5
            elif temp_size == 32 and "http" not in ioc:
                temp_row = [temp_date,temp_title,'MD5',ioc]
                writer.writerow(temp_row)
            elif "http" in ioc:
                temp_row = [temp_date,temp_title,'URL',ioc]
                writer.writerow(temp_row)
            else:
                temp_row = [temp_date,temp_title,'IP',ioc]
                writer.writerow(temp_row)
        print("-------------------------------------------\n")

    print("done")

    # sha256 64 chars
    # sha1 40 chars
    #MD5 32 chars
    # url contains http://
    # domain contains
    # ip contains 4 .