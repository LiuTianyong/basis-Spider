from lxml import etree
import requests
import time
import csv

fp = open('爱奇艺vip电影.csv','wt',newline='',encoding='UTF-8')
writer = csv.writer(fp)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.12 Safari/537.36'}
def get_info(url):
    res = requests.get(url,headers=headers)
    selector = etree.HTML(res.text)
    titles = selector.xpath('/html/body/div[3]/div/div/div[3]/div/ul/li/div[1]/a/@title')
    urls = selector.xpath('/html/body/div[3]/div/div/div[3]/div/ul/li/div[1]/a/@href')
    for title,url in zip(titles,urls):
        # writer.writerow((title,url))
        print(title,url)

if __name__ == '__main__':
    urls = ['http://list.iqiyi.com/www/1/----------2---11-{}-1-iqiyi--.html'.format(i) for i in range(0, 30)]
    for url in urls:
        get_info(url)
    fp.close()

