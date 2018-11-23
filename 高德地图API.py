import csv
import requests
import time

count = 0

while True:
    myTime = time.ctime()
    myTime = myTime.split(' ')[2:]
    myTime = myTime[-1] + ',' + myTime[0] + ',' + myTime[-2].replace(':',',')
    print(myTime)
    path = '路段/'+myTime + '路况表.csv'
    writeFp1 = open(path,'wt',newline='',encoding='utf-8')
    writeFp = open('经纬度表.csv','wt',newline='',encoding='utf-8')
    writer = csv.writer(writeFp)
    writer1 = csv.writer(writeFp1)

    writer1.writerow(('ID','起点经度','起点维度','终点经度','终点维度',
                              '路段名','流畅指数','缓行指数','拥堵指数','未知指数','路况','路况描述'))

    myKey = 'e20f308f78d0262f6cc717c1004c56e7'
    if count >= 2000:
        myKey = '464e3523099b730f4a820be7408198be'

    url_ = 'http://restapi.amap.com/v3/traffic/status/rectangle?key='+myKey+'&rectangle='#121.315,31.195;121.32,31.2

    with open('BOT智能汽车技术赛的初赛A榜测试信息.csv','r',encoding='utf-8') as fp:
        for i in fp.readlines():
            count += 1
            #以序列为标识
            id = i.split(',')[0]

            #读入起点经纬度
            startLongitude = i.split(',')[-1].split('~')[0]
            startLatitude = i.split(',')[-2].split('~')[0]

            #读取终点经纬度
            destinationLongitude = i.split(',')[-1].split('~')[-1]
            destinationLatitude = i.split(',')[-2].split('~')[-1]

            writer.writerow((id,startLongitude,startLatitude,destinationLongitude.split('\n')[0],destinationLatitude),)
            url = url_+startLongitude+ ',' + startLatitude + ';' + destinationLongitude.split('\n')[0] + ',' + destinationLatitude
            res = requests.get(url)
            res = res.json()
            print(res)
            if res['status'] == '0':
                continue
            returnDict = res['trafficinfo']

            #路段名称
            pathName = returnDict['description']
            #交通状态
            status_ = returnDict['evaluation']

            '''
            0：未知
            1：畅通
            2：缓行
            3：拥堵
            '''
            s = status_['status']
            if s == '1':
                status = '通畅'
            elif s == '2':
                status = '缓行'
            elif s == '3':
                status = '拥挤'
            else:
                status = '未知'
            #畅通指数
            expedite = status_['expedite']
            #缓行指数
            congested = status_['congested']
            #拥堵指数
            blocked = status_['blocked']
            #未知路段所占比例
            unknown = status_['unknown']

            #道路描述
            description = status_['description']

            writer1.writerow((id,startLongitude,startLatitude,destinationLongitude.split('\n')[0],destinationLatitude,
                            pathName,expedite,congested,blocked,unknown,status,description))
    break;
    #time.sleep(1800)