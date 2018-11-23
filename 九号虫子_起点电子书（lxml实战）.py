from lxml import etree
import requests
import time
import csv

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}



def info_get(url):
    res = requests.get(url)
    selector = etree.HTML(res.text)

    for i in range(1,20):
        books = selector.xpath('/html/body/div[2]/div[5]/div[2]/div[2]/div/ul/li[{}]/div[2]/h4/a/text()'.format(i))     #书名
        authors = selector.xpath('/html/body/div[2]/div[5]/div[2]/div[2]/div/ul/li[{}]/div[2]/p[1]/a[1]/text()'.format(i))     #作者
        categorys = selector.xpath('/html/body/div[2]/div[5]/div[2]/div[2]/div/ul/li[{}]/div[2]/p[1]/a[2]/text()'.format(i))   #类别
        labels = selector.xpath('/html/body/div[2]/div[5]/div[2]/div[2]/div/ul/li[{}]/div[2]/p[1]/a[3]/text()'.format(i))      #标签
        states = selector.xpath('/html/body/div[2]/div[5]/div[2]/div[2]/div/ul/li[{}]/div[2]/p[1]/span/text()'.format(i))      #连载情况
        summarizes = selector.xpath('/html/body/div[2]/div[5]/div[2]/div[2]/div/ul/li[{}]/div[2]/p[2]/text()'.format(i))       #概述
        writer.writerow((books, authors, categorys, labels, states, summarizes))
if __name__ == '__main__':
    urls = ['https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page={}'.format(number)for number in range(1,44821)]#44821
    for url in urls:
        info_get(url)
        time.sleep(1)
fp.close()
print('大哥，你交代的事情小虫虫我已经完成!')
