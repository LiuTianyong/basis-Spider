import re
import requests
import time
import random
from lxml import etree
import csv
from selenium import webdriver

fp = open('众筹\众筹区块链.csv','a+',newline='',encoding='UTF-8')
writer = csv.writer(fp)
writer.writerow(('项目名称','项目发起人/发起人','点赞数','支持数','已筹款','筹款进度','目标筹资','性质','地区','关键词',
                 '项目更新数量','项目更新详情','项目开始时间','项目结束时间','项目详情（详情中的所有文字）',
                 '是否有图片','是否有视频','评论数量','评论详情','无私支持数量','捐款记录'))

User_Agent = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:11.0) Gecko/20100101 Firefox/11.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR ',
    'Opera/9.80 (Windows NT 6.1; WOW64; U; zh-cn) Presto/2.10.229 Version/11.62',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
]                                       #加入请求头文件
headers = {
    'User-Agent':random.choice(User_Agent)
}

def commentAndRecord(id,myDict):
    headers = {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'DNT':'1',
        'Host':'www.zhongchou.cn',
        'Pragma':'no-cache',
        'Referer':'http://www.zhongchou.cn/browse/re-p2',
        'X-Requested-With':'XMLHttpRequest',
        'User-Agent': random.choice(User_Agent)
    }
    #爬取募捐记录
    #http://www.zhongchou.cn/deal-support_list?id=410971&page_size=10000&offset=0
    commentUrl = 'http://www.zhongchou.cn/deal-support_list?id={}&page_size=10000&offset=0'.format(id)

    commentRes = requests.get(commentUrl,headers = headers)
    commentRes = commentRes.json()
    commentRes = commentRes['data']['support_list']

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'www.zhongchou.cn',
        'Pragma': 'no-cache',
        'Referer': 'http://www.zhongchou.cn/browse/re-p2',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': random.choice(User_Agent)
    }
    recordUrl = 'http://www.zhongchou.cn/deal-topic_list?id={}&offset=0&page_size=10000'.format(id)
    recordRes = requests.get(recordUrl,headers = headers)
    recordRes = recordRes.json()
    recordRes = recordRes['data']['topic_list']

    #更新内容请求
    updateRecordUrl = 'http://www.zhongchou.cn/deal-march_list?id={}&offset=0&page_size=100'.format(id)
    updateRecordRes = requests.get(updateRecordUrl,headers=headers)
    updateRecordRes = updateRecordRes.json()
    updateRecordRes = updateRecordRes['data']['march_list']

    #项目开始时间
    try:
        projectStart = updateRecordRes[-1]['create_time']
        #项目结束时间
        projectEnd = updateRecordRes[0]['create_time']

    except:
        projectStart = '无'
        # 项目结束时间
        projectEnd = '无'
        pass
    print(projectStart,projectEnd)
    #项目更新
    v = ''
    for k in updateRecordRes:
        #更新时间
        updateTime = k['create_time']
        #更新内容
        updateComment = k['log_info']
        v = v + '\n' + updateTime + '\t' + updateComment + '\n'

    c = ''
    for j in recordRes:
        #评论内容
        comment = j['log_info']
        #评论者
        commentAuthor = j['user_name']
        #评论时间
        commentTime = j['create_time']
        c = c + commentAuthor + '\n' + commentTime + '\n' + comment + '\n'

    h = ''
    for i in commentRes:
        #捐款人名
        userName = i['user_name']
        #捐款金额
        userMoney = i['deal_price']
        #捐款类型
        userType = i['return_type']
        if userType == 0:
            userType = '有偿捐款'
        else:
            userType = '无偿捐款'
        #捐款日期
        userTime = i['pay_time']
        h = h + userName + '\n' + userMoney + '\n' + userType + '\n' + userTime + '\n'

    #print(myDict,c,h)
    '''
              '项目名称':projectName,
              '项目性质':'公益',
              '项目发起人':initiator,
              '关注度':attentionNum,
              '关键字':keyWord,
              '无私捐赠':selflessnessNum,
              '支持数量':poll,
              '募捐金额':moneyNum,
              '进度':plas,
              '地点':site,
              '项目更新数量':updateNum,
              '评论数量':commmentNum,
              '团队介绍':projectTeam,
              '照片':img,
              '视频':avi
    '''
    writer.writerow((myDict['项目名称'], myDict['项目发起人'], myDict['关注度'], myDict['支持数量'],
                     myDict['募捐金额'], myDict['进度'], myDict['目标金额'], myDict['项目性质'], myDict['地点'],
                     myDict['关键字'],myDict['项目更新数量'], v, projectStart,
                     projectEnd, myDict['团队介绍'],myDict['照片'], myDict['视频'],
                    myDict['评论数量'], c, myDict['无私捐赠'], h))

def info(url):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'www.zhongchou.cn',
        'Pragma': 'no-cache',
        'Referer': 'http://www.zhongchou.cn/browse/re-p2',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': random.choice(User_Agent)
    }
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    selector = etree.HTML(res.text)
    #票数
    poll = selector.xpath('//*[@id="jlxqOuterBox"]/div/div[1]/div[2]/div[2]/div[1]/div[1]/p/span[1]/text()')
    #已有金额
    moneyNum = selector.xpath('//*[@id="jlxqOuterBox"]/div/div[1]/div[2]/div[2]/div[1]/div[2]/p/span[1]/text()')
    #进度
    plas = selector.xpath('//*[@id="jlxqOuterBox"]/div/div[1]/div[2]/div[2]/div[2]/p/text()')
    #地址
    site = selector.xpath('//*[@id="jlxqOuterBox"]/div/div[1]/div[2]/div[2]/div[3]/div[2]/div/span[2]/a/text()')
    #项目名称
    projectName = selector.xpath('//*[@id="move"]/text()')
    #关注
    attentionNum = selector.xpath('//*[@id="jlxqOuterBox"]/div/div[1]/div[2]/div[1]/a/text()')
    #发起人
    #//*[@id="jlxqOuterBox"]/div/div[1]/div[1]/div/div[2]/span[2]/font
    initiator = selector.xpath('//*[@id="jlxqOuterBox"]/div/div[1]/div[1]/div/div[2]/span[2]/font/text()')
    #项目更新数量
    updateNum = selector.xpath('//*[@id="xqTabNav_ul"]/li[2]/b/text()')
    #关键字
    keyWord = selector.xpath('//*[@id="jlxqOuterBox"]/div/div[1]/div[2]/div[2]/div[3]/div[2]/div/span[3]/a/text()')
    #评论数量
    commmentNum = selector.xpath('//*[@id="xqTabNav_ul"]/li[3]/b/text()')
    #团队项目
    #//*[@id="xmxqBox"]/p[2]
    #//*[@id="xmxqBox"]/p[8]
    #//*[@id="xmxqBox"]/p[26]/text()  //*[@id="xmxqBox"]/p[47]
    projectTeam = selector.xpath('//*[@id="xmxqBox"]/p/text()')
    #无私支持人数
    selflessnessNum = selector.xpath('//*[@id="right"]/div/div[1]/div[1]/div/div[1]/h3/b/text()')
    #目标金额
    targetMoney = selector.xpath('//*[@id="jlxqOuterBox"]/div/div[1]/div[2]/div[2]/div[2]/div[2]/span[2]/b/text()')
    #是否存在图片
    #//*[@id="xmxqBox"]/img[3]  //*[@id="xmxqBox"]/img[1]
    #//*[@id="xmxqBox"]/img[1]
    projectImg = selector.xpath('//*[@id="xmxqBox"]/img[1]/@data-src')
    if len(projectImg):
        img = '是'
    else:
        img = '否'

    projectAvi = selector.xpath('//*[@id="left"]/a/div/img/@src')
    if len(projectAvi):
        avi = '是'
    else:
        avi = '否'
    #项目ID
    id = re.findall('\d+',url)[0]
    mydict = {'项目名称':projectName,
              '项目性质':'区块链',
              '项目发起人':initiator,
              '关注度':attentionNum,
              '关键字':keyWord,
              '无私捐赠':selflessnessNum,
              '支持数量':poll,
              '募捐金额':moneyNum,
              '目标金额':targetMoney,
              '进度':plas,
              '地点':site,
              '项目更新数量':updateNum,
              '评论数量':commmentNum,
              '团队介绍':projectTeam,
              '照片':img,
              '视频':avi
              }
    commentAndRecord(id,mydict)

def info_url(url):
    driver = webdriver.Chrome()  # 选择谷歌浏览器
    driver.maximize_window()  # 浏览器窗口最大化
    driver.get(url)
    driver.implicitly_wait(10)
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'www.zhongchou.cn',
        'Pragma': 'no-cache',
        'Referer': 'http://www.zhongchou.cn/browse/re-p2',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': random.choice(User_Agent)
    }

    res = requests.get(url,headers = headers)
    selector = etree.HTML(res.text)
    #//*[@id="ng-app"]/body/div[6]/div/div[1]/a
    urls = selector.xpath('//*[@id="ng-app"]/body/div[6]/div/div/a/@href')
    driver.close()
    print(urls)
    for url in urls:
        info('http://www.zhongchou.cn/deal-show/id-744137')



if __name__ == '__main__':
    li = [16]
    urls = ['http://www.zhongchou.cn/browse/id-22-re-p{}'.format(i) for i in li]
    for url in urls:
        print('***************************************测试靓仔******************************************')
        print('****************************************第{}页*******************************************'.format(url))
        info_url(url)
        time.sleep(random.randrange(3,6)+random.randrange(-3,3))


    fp.close()
    #补9,16,18,21,25,26,28,40