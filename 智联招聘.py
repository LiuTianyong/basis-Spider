import requests
import re
import time
from lxml import etree
import csv
import random

fp = open('智联招聘.csv','wt',newline='',encoding='UTF-8')
writer = csv.writer(fp)
'''地区，公司名，学历，岗位描述，薪资，福利，发布时间，工作经验，链接'''
writer.writerow(('职位','公司','地区','学历','岗位','薪资','福利','工作经验','链接'))

def info(url):
    res = requests.get(url)
    u = re.findall('<meta name="mobile-agent" content="format=html5; url=(.*?)" />', res.text)
    if len(u) > 0:
        u = u[-1]
    else:
        return
    headers ={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    res = requests.get(u,headers=headers)
    selector = etree.HTML(res.text)

    # '''地区，公司名，学历，岗位描述，薪资，福利，发布时间，工作经验，链接'''
    # #岗位名称
    # title = re.findall('<h1>(.*?)</h1>',res.text,re.S)
    title = selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[1]/h1/text()')
    # #岗位薪资
    # pay = re.findall('<li><span>职位月薪：</span><strong>(.*?)&nbsp',res.text,re.S)
    pay = selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[1]/div[1]/text()')
    # #工作地点
    # place = re.findall('<li><span>工作地点：</span><strong><a target="_blank" href=".*?">(.*?)</a>(.*?)</strong></li>',res.text,re.S)
    place = selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[3]/div[1]/span[1]/text()')
    # #发布时间
    # freshdate = re.findall('<li><span>发布日期：</span><strong><span id="span4freshdate">(.*?)</span></strong></li>',res.text,re.S)
    # #公司名称
    # companyName = re.findall('var Str_CompName = "(.*)";',res.text)[-1]
    campanyName = selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[2]/text()')
    # #学历
    # edu = re.findall('<li><span>最低学历：</span><strong>(.*?)</strong></li>',res.text)
    edu = selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[3]/div[1]/span[3]/text()')
    # #福利
    # welfare = re.findall('<div style="width:683px;" class="welfare-tab-box"> <span>(.*?)</span><span>(.*?)</span><span>(.*?)</span><span>(.*?)</span><span>(.*?)</span><span>(.*?)</span><span>(.*?)</span><span>(.*?)</span> </div>',res.text,re.S)
    walfare = selector.xpath('//*[@id="r_content"]/div[1]/div/div[3]/span/text()')
    # #工作经验
    # workEx = re.findall('<li><span>工作经验：</span><strong>(.*?)</strong></li>',res.text)
    # siteUlr = re.findall('<link rel="canonical" href="(.*?)" />',res.text)
    siteUrl = res.url
    workEx = selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[3]/div[1]/span[2]/text()')
    # #岗位详细
    # comment = re.findall('font-family: .*?;">(.*?)</span>',res.text,re.S)
    comment = selector.xpath('//*[@id="r_content"]/div[1]/div/article/div/p/text()')
    writer.writerow((title, campanyName, place, edu, comment, pay, walfare, workEx, siteUrl))
    print(title, campanyName, place, edu, comment, pay, walfare, workEx, siteUrl)
def infoUrl(url):
    res = requests.get(url)
    selector = res.json()
    code = selector['code']
    if code == 200:
        data = selector['data']['results']
        for i in data:
            href = i['positionURL']
            info(href)
            time.sleep(random.randrange(1,5))


if __name__ == '__main__':
    key = 'java'
    urls = ['https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=60&cityId=489&kw='.format(i*60)+key+'&kt=3&lastUrlQuery=%7B%22p%22:{},%22pageSize%22:%2260%22,%22jl%22:%22489%22,%22kw%22:%22java%22,%22kt%22:%223%22%7D'.format(i) for i in range(1,50)]
    for url in urls:
        infoUrl(url)