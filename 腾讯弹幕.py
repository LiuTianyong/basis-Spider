
import requests
import re
import csv
import time

def info(url):
    headers ={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
        }

    res = requests.get(url,headers=headers)

    r = re.findall('"content":"(.*?)"',res.text,re.S)
    for i in r:
        try:
            with open('还珠格格/试色幸也.csv','a') as fp:
                fp.write(i)
                fp.write('\n')
        except:
            pass

if __name__ == '__main__':
    ur = 'https://mfm.video.qq.com/danmu?otype=json&callback=jQuery1910895541880946169_1534140358559&timestamp={}'
    u = '&target_id=2457656528&count=80&second_count=5&session_key=108383%2C580%2C1534140358&_=15341403{}'
    i = 45
    j = 58590
    l = 1
    while True:
        if j > 68590:
            break
        url = ur.format(i) + u.format(j)
        print(url)
        info(url)
        i += 30
        j += 1
        l += 1
        print(l)
