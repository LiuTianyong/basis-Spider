import re
import requests
import time

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}

f = open('C:/Users/Administrator/Desktop/斗破苍穹.txt','a+')

def get_info(url):
    res = requests.get(url,headers = headers)
    if res.status_code == 200:
        contents = re.findall('<p>(.*?)</p>',res.content.decode('GBK'),re.S)
        for content in contents:
            f.write(content+'\n')
    else:
        pass
if __name__ == '__main__':
    urls = ['http://www.31xs.net/2/2500/{}.html'.format(str(i)) for i in range(5868638,5870261)]
    for url in urls:
        get_info(url)
        time.sleep(1)
f.close()
print("爬取完毕")