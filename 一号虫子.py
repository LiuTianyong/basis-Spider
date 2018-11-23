import requests
from bs4 import BeautifulSoup
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}
res = requests.get('http://bj.xiaozhu.com/',headers = headers)                    #访问小猪短租网站
soup = BeautifulSoup(res.text,'html.parser')
prices = soup.select('#page_list > ul > li > div.result_btm_con.lodgeunitname > span.result_price > i')
#soup.find_all('div','item')                                                         #查找div标签，class = 'item
for i in prices:
    print(i.get_text())                                                              #通过get_text获取文字信息——取掉标签
