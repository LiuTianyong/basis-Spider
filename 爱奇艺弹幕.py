import requests
import json
import re
import csv
import time
import random

def info(url):
    fp = open('爱奇艺/爱奇艺.csv', 'a',encoding='utf-8')
    headers ={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
    }
    res = requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    print(res.text)
    r = re.findall('"description":"(.*?)"',res.text,re.S)
    num = re.findall('"tvTitle":"为了你我愿意热爱整个世界第(\d+)集"',res.text,re.S)
    for i,j in zip(num,r):
        fp.write(i)
        fp.write(j)
        fp.write('\n')

    fp.close()

if __name__ == '__main__':
    urls = ['http://api-t.iqiyi.com/feed/get_feeds?&agenttype=118&wallId=259595647&count=50&top=1&hasRecomFeed=1&feedId=94628937748&needTotal=1&notice=1&version=1&upOrDown=1&snsTime=153408{}'.format(random.randrange(2000,5000))+'&_=153408{}'.format(i) for i in range(3878316,4878316)]
    for url in urls:
        print(url)
        info(url)
        time.sleep(random.randrange(1,3))
        