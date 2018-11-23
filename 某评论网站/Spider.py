import requests
from lxml import etree
import csv
import numpy as np


fp = open('评论.csv','a+',newline='',encoding='UTF-8')
writer = csv.writer(fp)
writer.writerow(('标题','星级','内容','标签'))

#https://www.tripadvisor.com/Airline_Review-d8729046-Reviews-or70-Cathay-Pacific#REVIEWS
urls = ['https://www.tripadvisor.com/Airline_Review-d8729046-Reviews-or{}-Cathay-Pacific#REVIEWS'.format(i) for i in range(0,4001,10)]

for url in urls:
    print(url)
    # 1.评论标题  2.评价的星级  3.评论内容 4.评论标签
    res = requests.get(url)
    selector = etree.HTML(res.text)

    titles = selector.xpath('//*[@class="quote isNew"]/a/span/text()')
    stars = selector.xpath('//*[@class="rating reviewItemInline"]/span[1]/@class')
    comments = selector.xpath('//*[@class="partial_entry"]/text()')
    tags = selector.xpath('//*[@class="allLabels"]/span/text()')
    if len(titles) == 0:
        titles = selector.xpath('//*[@class="quote"]/a/span/text()')
    if len(tags) == 30:
        tags = np.array(tags).reshape((10,3))
    else:
        while len(tags) < 30:
            tags.append('NULL')
    for title, star, comment, tag in zip(titles, stars, comments, tags):
        print(title, star, comment, tag)
        writer.writerow((title, star, comment, tag))
fp.close()