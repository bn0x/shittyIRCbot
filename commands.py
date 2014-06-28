import requests
from bs4 import BeautifulSoup

def isItUp(website):
    if website.startswith("http://") or website.startswith("https://"):
        pass
    else:
        website = "http://%s"%website

    try:
        request = requests.get(website)
    except:
        return "[-] %s is currently down!"%website

    if request.status_code < 210:
        return "[+] %s is currently up!"%website
    else:
        return "[-] %s is currently down!"%website

def websiteTitle(website):
    try:
        request = requests.get(website)
        bs = BeautifulSoup(request.text)
        return bs('title')[0].text.encode('utf-8')
    except: return None