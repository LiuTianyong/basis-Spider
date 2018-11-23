from bs4 import BeautifulSoup
import requests
import csv
import re
import time


writer = csv.writer(fp)
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}

def info(url):
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text,'lxml')
    comments = soup.select('#comments > div > div.comment > p > span')
    print(res.url)
    for comment in comments:
        comment = re.findall('<span class="short">(.*?)</span>',str(comment))
        print(comment)



if __name__ == '__main__':
    urls = ['https://movie.douban.com/subject/26752088/comments?start={}&limit=20&sort=new_score&status=P'.format(i) for i in range(0,481,20)]
    for url in urls:
        info(url)
        time.sleep(1)