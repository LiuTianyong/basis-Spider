import requests
from lxml import etree
import re

fp = open('明星.txt','a+',encoding='utf-8')
def info(url):
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'
    }
    res = requests.get(url,headers=headers)
    names = re.findall('<h2>(.*?)</h2>',res.text)
    for name in names:
        fp.write(name+'\n')
        print(name)

if __name__ == '__main__':
    urls = ['http://www.ylq.com/star/list-all-------{}.html'.format(i) for i in range(1,153)]
    for url in urls:
        info(url)