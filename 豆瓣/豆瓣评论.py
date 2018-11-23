import requests
from lxml import etree

headers ={                                                       #加入头请求
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}
fp = open('豆瓣.txt','a+',newline='',encoding='UTF-8')

def info(url):
    res = requests.get(url, headers= headers)
    res.encoding = 'utf-8'
    selector = etree.HTML(res.text)
    comments = selector.xpath('//*[@class="short-content"]/text()')
    for comment in comments:
        print(comment.strip())
        fp.writelines(comment)
if __name__ == '__main__':
    urls = ['https://movie.douban.com/subject/3168101/reviews?start={}'.format(i) for i in range(0, 920, 20)]
    for url in urls:
        info(url)
