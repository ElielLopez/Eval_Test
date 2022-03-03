# Evaluation Test
### Virus Total Score
-----------------
This program will recieve a file or a file path from the user and checks if more then 50 engines detected it as malicious <br/>
or Check Point engine\ Microsoft engine detected it as malicious <br/>

requirements:
1. Install requests
2. Install Flask 
3. install iocextract 
4. install bs4
5. install feedparser<br/>

To run the program, you must insert your VT API key and a file name or a path to the file <br/>
for example:
![cmd_exm](https://user-images.githubusercontent.com/58383829/156204152-45e1bdec-ab36-4cce-b52f-0510dcd4fb24.jpg)
<br/>

notice that you must write **_-k_** and **_-i_** <br/>

#### Engine detection
![engine detection](https://user-images.githubusercontent.com/58383829/156322546-1e5070f1-a19d-4132-93c4-32bb9d8f852a.jpg)


### Check Point Research Feed
-----------------
This script will web scrap Check Point RSS feed and parse recent publications.<br/> After parsing the data, the script will write the released date, title and author<br/> to a file named **__publication_summary__** and straight to the terminal for more convinience.
![publication summary](https://user-images.githubusercontent.com/58383829/156600531-31485fe7-7ff6-4487-bd92-58d744722838.jpg)


IOC will be extracted from each article into a CSV file named **__IOC_csv_file__** in the following format: Date | Title | IOC_Type | IOC <br/>
![csv file](https://user-images.githubusercontent.com/58383829/156600085-95fdd50e-797e-4b3a-ab3a-407338291d0d.jpg)


Creating text file named **__IOCs_Link__** with all the links of the articles that contains IOCs with time stamp for further reading and deeper investigation <br/>
![ioc txt file with timestamp](https://user-images.githubusercontent.com/58383829/156553173-bc9e23f5-9d08-4142-bb2a-19039b56e07e.jpg)



_________________
