from lxml import etree
import requests
import time
import re
import csv

fp = open('C://Users/Administrator/Desktop/博客.csv','wt',newline='',encoding='UTF-8')
writer = csv.writer(fp)
writer.writerow(('地点','想去的人数','去过的人数',))

def info(url):
    res = requests.get(url)
    selector = etree.HTML(res.text)
    url_infos = selector.xpath('/html/body/div[5]/div[1]/div[2]/ul')

    for url_info in url_infos:
        #places = selector.xpath('/html/body/div[5]/div[1]/div[2]/ul/li[{}]/a/span/text()'.format(j))
        '''获取的信息为火星文  原因不明  用正则代替'''
        places = re.findall('<img alt="(.*?)"',res.content.decode('UTF-8'),re.S)
        #<span>厦门市</span>
        # <img alt="厦门市" src="http://storage.travel.sina.com.cn/jingdian/201309171806075540_20110425_142142_default_180.jpg">
        wants = url_info.xpath('li/p/span[1]/em/text()')
        beens = url_info.xpath('li/p/span[2]/em/text()')
        for place,want,been in zip(places,wants,beens):
            print(place+'\t'+want+'\t'+been)
            writer.writerow((place, want, been))
def info_s(url):
    res = requests.get(url)
    selector = etree.HTML(res.text)
    url_infos = selector.xpath('/html/body/div[5]/div[1]/div[3]/div[1]')
    for url_info in url_infos:
        places = url_info.xpath('')

if __name__ == '__main__':
    urls = ['http://travel.sina.com.cn/zhongguo-chengshi-lvyou/pn-{}/'.format(i)for i in range(1,50)]
    urls_1 = ['http://travel.sina.com.cn/zhongguo-jingqu-lvyou/pn-{}/'.format(i)for i in range(1,71)]
    for url in urls:
        info(url)
        time.sleep(1)
    writer.writerow(('---------------------------------------------------------'))          #分界线
    for url in urls_1:
        info(url)
        time.sleep(1)


