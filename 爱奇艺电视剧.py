import requests
from lxml import etree
import csv
import time                        #导入相应的库

#写入数据的头
fp = open('C://Users/Administrator/Desktop/爱奇艺电视剧.csv','wt',newline='',encoding='UTF-8')
writer = csv.writer(fp)
writer.writerow(('电视剧名称','地点','全集数','导演','类型','语言','电视台','年份','播放量','简介','演员','评论数'))

#头伪装
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}

TV = {}

def info(url):
    res = requests.get(url,headers = headers)
    selector = etree.HTML(res.text)
    info_urls = selector.xpath('/html/body/div[3]/div/div/div[3]/div/ul')
    for info_url in info_urls:
        urls = info_url.xpath('li/div[1]/a')
        for url in urls:
            href = url.xpath('./@href')[0]
            #print(href,'**********此时一个靓仔路过测试***********************************')
            info_s(href)
    pass

def info_s(url):                #由于URL无规律可循不可构建URL列表   通过info_s函数爬取url 构造url列表 进行爬取
    res = requests.get(url,headers = headers)
    selector = etree.HTML(res.text)

    names = selector.xpath('//*[@id="block-BB"]/div/div[1]/div/h1/a[1]/text()')                         #电视剧名称
    #print(names, '**********此时一个路过一个测试的靓仔***********************************')
    place = selector.xpath('//*[@id="block-BB"]/div/div[1]/div/div[3]/div[1]/div[1]/p[1]/a/text()')    #地区
    sum_num = selector.xpath('//*[@id="block-BB"]/div/div[1]/div/div[2]/span/em/text()')                #全集数
    director = selector.xpath('//*[@id="block-BB"]/div/div[1]/div/div[3]/div[1]/div[1]/p[2]/a/text()') #导演
    types = selector.xpath('//*[@id="block-BB"]/div/div[1]/div/div[3]/div[1]/div[2]/p[1]')              #类型
    #//*[@id="block-BB"]/div/div[1]/div/div[3]/div[1]/div[2]/p[1]/a[2]
    for type in types:
        if type != None:
            type_ = type.xpath('a/text()')
            #print(type_, '**********此时路过一个测试的靓仔***********************************')
            #for str in type_:
                #print(str,'**********此时路过一个测试的靓仔***********************************')
        else:
            pass

    language = selector.xpath('//*[@id="block-BB"]/div/div[1]/div/div[3]/div[1]/div[2]/p[2]/a/text()')  #语言
    TV_station = selector.xpath('//*[@id="block-BB"]/div/div[1]/div/div[3]/div[1]/div[2]/p[3]/span/text()')#电视台
    year = selector.xpath('//*[@id="block-BB"]/div/div[1]/div/div[3]/div[1]/div[2]/p[4]/a/text()')          #上市年份
    play_amount = selector.xpath('//*[@id="movie-score-show"]/span[1]/text()')                                #播放量
    summarize = selector.xpath('//*[@id="block-BB"]/div/div[1]/div/div[3]/div[3]/span/text()')               #简介
    #comment = selector.xpath('//*[@id="movie-score-show"]/span[2]/i[1]/text()')
    '''评分不能爬取   此bug有待修复        #<i data-score-num="1">7</i>
    '''
    actors = selector.xpath('//*[@id="block-E"]/div[2]/ul')                                                     #演员
    for actor_ in actors:
        actor = actor_.xpath('li/div[2]/p[1]/a/text()')
    evaluationNum = selector.xpath('//*[@id="widget-tab-0"]/div[2]/div[2]/div/div[1]/div/div[1]/span/text()')#评论数量
    print('****************************************靓仔正在爬取************************************************')

    try:
        TV = {
            'names':names,
            'place':place,
            'sum_num':sum_num,
            'director':director,
            'type':type_,
            'language':language,
            'TV_station':TV_station,
            'year':year,
            'play_amount':play_amount,
            'summarize':summarize,
            'actor':actor,
            'evaluationNum':evaluationNum
        }
    except:
        pass
    try:
        writer.writerow((names, place, sum_num, director, type_, language, TV_station, year,play_amount,summarize,actor,evaluationNum))
    except:
        pass

def PL_info(url):                   #该函数爬取各个电视剧所有评论
    #改日再写
    pass

if __name__ == '__main__':
    '''
    http://list.iqiyi.com/www/2/-------------11-1-1-iqiyi--.html
    http://list.iqiyi.com/www/2/-------------11-2-1-iqiyi--.html
    ……
    http://list.iqiyi.com/www/2/-------------11-30-1-iqiyi--.html
    '''
    urls = ['http://list.iqiyi.com/www/2/-------------11-{}-1-iqiyi--.html'.format(i) for i in range(1,30)]

    for url in urls:
        info(url)
        time.sleep(1)

    fp.close()
    print('***********************执行完毕******************')
