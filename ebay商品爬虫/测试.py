import requests
from lxml import etree
import re

headers ={                                                       #加入头请求
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}

url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=iphone+xs+screen+protector'
res = requests.get(url,headers)
print(res.text)
selector = etree.HTML(res.text)
print(selector.xpath('//*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/a/h2/text()'))