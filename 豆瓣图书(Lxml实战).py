
from lxml import etree
import requests
import time
import csv

fp = open('C://Users/Administrator/Desktop/douban.csv','wt',newline='',encoding='UTF-8')
writer = csv.writer(fp)
writer.writerow(('书名','作者','译者','类别','评分','评论人数','内容概述','定价'),)

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}

def info_get(url):
    res = requests.get(url)
    selector = etree.HTML(res.text)
    books = selector.xpath('/html/body/div/div/article/div[2]/div[1]/ul/li[1]/div[2]/div[2]/a/text()')#书名
    authors = selector.xpath('/html/body/div/div/article/div[2]/div[1]/ul/li[1]/div[2]/p[1]/span[1]/span[2]/a/text()')#作者
    translators = selector.xpath('/html/body/div/div/article/div[2]/div[1]/ul/li[1]/div[2]/p[1]/span[2]/span[2]/a/text()')#译者
    categorys = selector.xpath('/html/body/div/div/article/div[2]/div[1]/ul/li[2]/div[2]/p[2]/span/span[2]/span/text()')#类别
    grades = selector.xpath('/html/body/div/div/article/div[2]/div[1]/ul/li[1]/div[2]/div[3]/span[2]/text()')#评分
    observer_numbers = selector.xpath('/html/body/div/div/article/div[2]/div[1]/ul/li[1]/div[2]/div[3]/span[3]/a/span/text()')#评论人数
    summarizes = selector.xpath('/html/body/div/div/article/div[2]/div[1]/ul/li[1]/div[2]/div[4]/text()')#内容概述
    prices = selector.xpath('/html/body/div/div/article/div[2]/div[1]/ul/li[1]/div[2]/div[1]/div/span/span/text()')#定价

    book_messages = {
        'books':books,
        'author':authors,
        'translators':translators,
        'categorys':categorys,
        'grades':grades,
        'observer_numbers':observer_numbers,
        'summarizes':summarizes,
        'prices':prices
    }

    writer.writerow((books,authors,translators,categorys,grades,observer_numbers,summarizes,prices))

if __name__=='__main__':
    urls = ['https://read.douban.com/k  ind/1?start={}'.format(number)for number in range(0,63600,20)]
    for url in urls:
        info_get(url)
        time.sleep(1)
fp.close()
print('大哥，小虫子我已经完成你交代的任务！')