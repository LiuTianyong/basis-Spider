import requests
from bs4 import BeautifulSoup
import bs4

def getHTMLText(url):
    kv = {'User-agent': 'Baiduspider'}
    try:
        r = requests.get(url, headers = kv, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''

def findPList(html):
    plist = []
    soup = BeautifulSoup(html, "html.parser")
    plist.append(soup.title.string)
    print(soup)
    for div in soup.find_all('div', attrs={"class": "bd doc-reader"}):
        plist.extend(div.get_text().split('\n'))

    plist = [c.replace(' ', '') for c in plist]
    plist = [c.replace('\x0c', '') for c in plist]
    return plist

def printPList(plist, path = 'baiduwenku.txt'):
    file = open(path, 'w')
    for str in plist:
        file.write(str)
        file.write('\n')
    file.close()

def main():

    url = 'https://wenku.baidu.com/view/3c5d5dd603d276a20029bd64783e0912a2167c94.html?from=search'
    html = getHTMLText(url)
    plist = findPList(html)
    printPList(plist)

main()