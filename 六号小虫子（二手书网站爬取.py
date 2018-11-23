from bs4 import BeautifulSoup
import requests
import time                                                     #导入相应的头文件

headers ={                                                       #加入头请求
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}

f = open('C:/Users/Administrator/Desktop/有路网.txt','a+')

def get_info(url):
    wb_data = requests.get(url,headers = headers)
    if wb_data.status_code == 200:
        #print(wb_data)
        soup = BeautifulSoup(wb_data.text,'lxml')
        #print(soup)
        titles = soup.select('#name > h2')

        for title in titles:
            data = {
                '书籍名字':title.get_text().strip(),
            }
            str = data['书籍名字']
            str = str.replace("",'')
            str = str.replace("",'')
            print(str)
            f.write(str+'\n')
if __name__ == '__main__':                                #定义程序入口
    urls = ['http://www.youlu.net/{}'.format(number)for number in range(57159,4000000)]
    for url in urls:
        print(url)
        get_info(url)
    time.sleep(1)
f.close()
print("爬取完毕")