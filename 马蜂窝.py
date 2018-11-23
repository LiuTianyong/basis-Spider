import requests
import re
import random
from lxml import etree
import time
import json
import csv


fp = open('马蜂窝用户.csv','a+',newline='',encoding='UTF-8')
writer = csv.writer(fp)
writer.writerow(('用户ID','用户等级','现居地址','回答数','金牌回答数','采纳率','关注人数','粉丝数量','蜂蜜'))

User_Agent = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:11.0) Gecko/20100101 Firefox/11.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR ',
    'Opera/9.80 (Windows NT 6.1; WOW64; U; zh-cn) Presto/2.10.229 Version/11.62',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
]
def info_list_url(url):
    headers = {
        'User-Agent':random.choice(User_Agent)
    }
    res = requests.get(url,headers=headers)
    res.encoding = 'UTF-8'
    res = res.json()
    #从目录中获取每个帖子url
    res = res['data']['html']
    ids = re.findall('<a href="/wenda/detail-(\d+).html" target="_blank">',res,re.S)
    for id in ids:
        info_url(id,1)
        time.sleep(random.randrange(1, 5))

def info_url(id,page):
    headers = {
        'User-Agent': random.choice(User_Agent)
    }
    url = 'http://www.mafengwo.cn/qa/ajax_qa/moreAnswer?page={}'.format(page) +'&qid={}.html'.format(id)

    res = requests.get(url,headers=headers)
    res = res.json()
    r = res['data']['has_more']
    if r == 1:
        res = res['data']['html']
        ids = re.findall('<a class="name" href="/wenda/u/(\d+)/answer.html"',res,re.S)
        for id in ids:
            info(id)
            time.sleep(random.randrange(1, 5))
            page = page +1
            info_url(id,page)

def info(id):
    headers = {
        'User-Agent': random.choice(User_Agent)
    }
    url = 'http://www.mafengwo.cn//wenda/u/{}/answer.html'.format(id)
    res = requests.get(url,headers=headers)
    selector = etree.HTML(res.text)

    '''
    等级、现居、回答数、金牌回答数、采纳率、关注人数、粉丝数量、蜂蜜
    '''
    #用户id
    id = selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/text()')
    #等级
    lv = selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[4]/span[1]/a/text()')
    #地址
    site = selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[4]/span[2]/text()')
    #回答数
    respensesNum = selector.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/ul/li[1]/a/strong/text()')
    #金牌回答数
    goldRespensesNum = selector.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/ul/li[2]/a/strong/text()')
    #采纳率
    adoptionRate = selector.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/ul/li[3]/strong/text()')
    #关注人数
    attentionNum = selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[7]/div[1]/strong/a/text()')
    #粉丝
    fansNum = selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[7]/div[2]/strong/a/text()')
    #蜜蜂
    bees = selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[7]/div[3]/strong/a/text()')

    print(id,lv,site,respensesNum,goldRespensesNum,adoptionRate,attentionNum,fansNum,bees)
    writer.writerow((id,lv,site,respensesNum,goldRespensesNum,adoptionRate,attentionNum,fansNum,bees))

if __name__ == '__main__':
    urls = ['http://www.mafengwo.cn/qa/ajax_qa/more?type=1&mddid=' \
            '&tid=&sort=10&key=&page={}&time='.format(i) for i in range(1,25)]
    for url in urls:
        info_list_url(url)
        time.sleep(random.randrange(1,5))

    fp.close()