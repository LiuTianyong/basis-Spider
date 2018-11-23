import requests
from lxml import etree
import random
import time
import csv


USER_AGENT = [
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:\'2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:\'2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; \'U; en) Pre\'sto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; \'U; en) Pre\'sto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'
]


def get_url(url):
    headers ={
        'User-Agent':random.choice(USER_AGENT)
    }
    try:
        res = requests.get(url,headers=headers,timeout=7)
    except:
        res = requests.get(url, headers=headers, timeout=7)

    selector = etree.HTML(res.text)
    urls = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/a/@href')
    for url in urls:
        get_info('https://block.cc'+url+'?tab=basic')

def get_info(url):
    fp = open('交易币.csv', 'a+', encoding='utf-8', newline='')
    writer = csv.writer(fp)

    headers = {
        'User-Agent': random.choice(USER_AGENT)
    }
    try:
        res = requests.get(url, headers=headers, timeout=7)
    except:
        res = requests.get(url, headers=headers, timeout=7)
    selector = etree.HTML(res.text)

    #IOC信息
    icoUrl = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[2]/div/div[1]/div[2]/h2/a/@href')
    if icoUrl:
        logo = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/img/@src')
        # 中文名
        chineseName = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/p/span[1]/text()')
        # 英文名
        englishName = selector.xpath(
            '//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/p/span[2]/text()')
        # 显示名称
        title = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/h1/text()')
        # 发行日期
        # //*[@id="app"]/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/p[1]/span[2]
        issueData = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[2]/div/div[1]/div[1]/div/p[2]/span[2]/text()')
        # 流通数量
        circulateNum = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[3]/dl[2]/dd[1]/text()')
        # 总发行量
        issueNum = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[3]/dl[2]/dd[3]/text()')
        # 官方地址
        officialUrl = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/a[1]/@href')
        # 简介
        briefIntroduction = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[2]/div/div[1]/div[3]/div/p[1]/text()')
        # 区块浏览1
        blockUrlOne = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/a[2]/@href')
        # 区块浏览2
        blockUrlTwo = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/a[3]/@href')
        # 白皮书
        whiteBook = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/a[8]/@href')
        # 相关概念
        #//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[2]/div/div[1]/div[1]/div/p[5]/span[2]
        relatedNotion = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[2]/div/div[1]/div[1]/div/p[5]/span[2]/a/span/text()')
        # 众筹价格
        raisePrice = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[2]/div/div[1]/div[2]/div/p[5]/span[2]/text()')
        # IOC信息
        icoUrl = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[2]/div/div[1]/div[2]/h2/a/@href')

        icoDict = get_ico('https://block.cc'+icoUrl[0])
        icoUrlStorage = 'https://block.cc'+icoUrl[0]
        icoStates = icoDict['icoStates'],
        icoTerrace = icoDict['icoTokenTerrace'] + icoDict['icoTeamAllocation'] + icoDict['icoCrowdAllocation'],
        icoSumNum = icoDict['icoSumNum']

        writer.writerow((logo, chineseName, englishName, title, issueData, circulateNum, issueNum,
              officialUrl, briefIntroduction, blockUrlOne, blockUrlTwo, whiteBook,
              relatedNotion, raisePrice,icoStates, icoTerrace, icoSumNum,icoUrlStorage))
        print(logo, chineseName, englishName, title, issueData, circulateNum, issueNum,
              officialUrl, briefIntroduction, blockUrlOne, blockUrlTwo, whiteBook,
              relatedNotion, raisePrice,icoStates, icoTerrace, icoSumNum,icoUrlStorage,'***************靓仔测试*******')
    else:
        logo = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/img/@src')
        # 中文名
        chineseName = selector.xpath(
            '//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/p/span[1]/text()')
        # 英文名
        englishName = selector.xpath(
            '//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/p/span[2]/text()')
        # 显示名称
        title = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/h1/text()')
        # 发行日期
        issueData = selector.xpath(
            '//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[2]/div/div[1]/div[1]/div/p[2]/span[2]/text()')
        # 流通数量
        circulateNum = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[3]/dl[2]/dd[1]/text()')
        # 总发行量
        issueNum = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[3]/dl[2]/dd[3]/text()')
        # 官方地址
        officialUrl = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/a[1]/@href')
        # 简介
        briefIntroduction = selector.xpath(
            '//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[2]/div/div[1]/div[2]/div/p/text()')
        # 区块浏览1
        blockUrlOne = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/a[2]/@href')
        # 区块浏览2
        blockUrlTwo = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/a[3]/@href')
        # 白皮书
        whiteBook = selector.xpath('//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/a[7]/@href')
        # 相关概念
        relatedNotion = selector.xpath(
            '//*[@id="app"]/div[1]/div[2]/div/div/div[1]/div[2]/div/div[1]/div[1]/div/p[5]/span[2]/a/span/text()')
        writer.writerow((logo, chineseName, englishName, title, issueData, circulateNum, issueNum,
                         officialUrl, briefIntroduction, blockUrlOne, blockUrlTwo, whiteBook,
                         relatedNotion))
        print(logo, chineseName, englishName, title, issueData, circulateNum, issueNum,
              officialUrl, briefIntroduction, blockUrlOne, blockUrlTwo, whiteBook,
              relatedNotion)
    fp.close()

def get_ico(url):
    headers = {
        'User-Agent': random.choice(USER_AGENT)
    }
    try:
        res = requests.get(url, headers=headers)
    except:
        res = requests.get(url, headers=headers, timeout=7)
    selector = etree.HTML(res.text)
    #ico状态
    icoStates = selector.xpath('//*[@id="sectionTeam"]/div/section/div/div/div/p/span/text()')
    #代币平台
    icoTokenTerrace = selector.xpath('//*[@id="sectionInfo"]/div/section[3]/ul/li[4]/span[2]/text()')
    #ioc团队分配
    icoTeamAllocation = selector.xpath('//*[@id="sectionInfo"]/div/section[2]/div/div[1]/ul/li[1]/p/text()')
    #ioc众筹分配
    icoCrowdAllocation = selector.xpath('//*[@id="sectionInfo"]/div/section[2]/div/div[1]/ul/li[2]/p/text()')
    #其他筹集
    icoOtherAllocation = selector.xpath('//*[@id="sectionInfo"]/div/section[2]/div/div[1]/ul/li[3]/p/text()')
    #ico总量
    icoSumNum = selector.xpath('//*[@id="sectionInfo"]/div/section[3]/ul/li[8]/span[2]/span/text()')
    icoDict ={
        'icoStates':icoStates,
        'icoTokenTerrace':icoTokenTerrace,
        'icoTeamAllocation':icoTeamAllocation,
        'icoCrowdAllocation':icoCrowdAllocation,
        'icoOtherAllocation':icoOtherAllocation,
        'icoSumNum':icoSumNum
    }
    return icoDict


if __name__ == '__main__':
    #64  65    66  67 68  69 70 72  73  74  75
    urls = ['https://block.cc/coin?page={}'.format(i) for i in range(0,78)]
    for url in urls:
        get_url(url)



