import requests
from lxml import etree
import csv

headers ={                                                       #加入头请求
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}

fp = open('兼职猫.csv','a+',newline='',encoding='UTF-8')
writer = csv.writer(fp)
writer.writerow(('岗位', '职业', '公司简介'))

def info(url):
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
    tietle = selector.xpath('/html/body/section/article/div/div[1]/div[2]/div[1]/h1/text()')
    job_type = selector.xpath('/html/body/section/article/div/div[1]/div[2]/div[1]/div[1]/a/text()')
    label = selector.xpath('/html/body/section/article/div/div[1]/div[3]/div[2]/div[1]/div[2]/p[1]/text()')
    print(tietle,job_type,label)
    writer.writerow((tietle,job_type,label))

if __name__ == '__main__':
    urls = ['http://guangzhou.jianzhimao.com/dbx_zbx_0/index{}.html'.format(i) for i in range(1,12)]
    for url in urls:
        res = requests.get(url, headers=headers)
        selector = etree.HTML(res.text)
        urls_ = selector.xpath('//*[@id="content_list_wrap"]/li/a/@href')
        for href in urls_:
            info('http://guangzhou.jianzhimao.com' + href)
