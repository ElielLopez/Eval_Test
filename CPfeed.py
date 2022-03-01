import flask
import requests
import urllib3

# url = "https://research.checkpoint.com/feed/"
if __name__ == '__main__':
    urllib3.disable_warnings()
    url = 'https://research.checkpoint.com/feed/'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.post(url, headers=headers)
    print(response.status_code)
    print(response.text)