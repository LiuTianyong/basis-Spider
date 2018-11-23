import requests
from lxml import etree
import re
import random


User_Agent = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:11.0) Gecko/20100101 Firefox/11.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR ',
    'Opera/9.80 (Windows NT 6.1; WOW64; U; zh-cn) Presto/2.10.229 Version/11.62',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
]                                       #加入请求头文件

def info(url):
    url_ = 'http://www.mouser.cn'
    url = url_ + url

    res = requests.get(url)
    selector = etree.HTML(res.text)
    print(res.text)

def info_url(url):
    headers = {  # 加入头请求
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
    }
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
    hrefOne = selector.xpath('//*[@class="SearchResultsRowOdd"]/td[3]/div/a/@href')
    hrefTwo = selector.xpath('//*[@class="SearchResultsRowEven"]/td[3]/div/a/@href')
    hrefs = hrefOne + hrefTwo

    for href in hrefs:
        info(href)


if __name__ == '__main__':
    # http://www.mouser.cn/Search/Refine.aspx?Keyword=RC0603FR-07200RL
    url = 'http://www.mouser.cn/Search/Refine.aspx?Keyword=BAT54A'
    info_url(url)