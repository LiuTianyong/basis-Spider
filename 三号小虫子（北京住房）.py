from bs4 import BeautifulSoup
import requests
import time                                                     #导入相应的头文件

headers ={                                                       #加入头请求
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}

def judgament_sex(class_name):                                   #定义判断用户的性别的函数
    if class_name == {'member_icol'}:
        return '女'
    else:
        return '男'

def get_links(url):
    #print(url)
    wb_data = requests.get(url,headers = headers)
    soup = BeautifulSoup(wb_data.text,'lxml')
    links = soup.select('#page_list > ul > li > a')                #links为ual列表
    for link in links:
        href = link.get("href")                               #循环出的url 一次调用get_info()函数
        get_info(href)

def get_info(url):
    wb_data = requests.get(url,headers = headers)
    soup = BeautifulSoup(wb_data.text,'lxml')
    tittles = soup.select('div.pho_info > h4')
    addresses = soup.select('span.pr5')

    prices = soup.select('#pricePart > div.day_1 > span')
    imgs = soup.select('#floatRightBox > div.js_box..clearfix>div.member_pic > a >img')
    names = soup.select('#floatRightBox > div.js_box..clearfix>div.w_240 > h6 >a')
    sexs = soup.select('#floatRightBox > div.js_box..clearfix>div.nember_pic > div')
    for tittle,addresse,price,img,name,sex in zip(tittles,addresses,prices,imgs,names,sexs):
        data = {
            'tittle':tittle.get_text().strip(),
            'address':addresse.get_text().strip(),
            'price':price.get_text(),
            'img':img.get("src"),
            'name':name.get_text(),
            'sex':judgament_sex(sex.get("class"))
        }
        print(data)                                            #获取信息并通过字典打印
if __name__ == '__main__':                                #定义程序入口
    urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(number)for number in range(1,14)]
    for i in urls:
        print(i)
    for single_url in urls:
        get_links(single_url)
    time.sleep(2)