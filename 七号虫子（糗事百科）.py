import requests
import re                                #导入相应的头文件

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}                                        #加入请求头文件

info_lists = []                          #初始化列表，用于装入爬虫信息

def judgment_sex(class_name):
    if class_name == 'womenIcon':
        return '女'
    else:
        return '男'

def get_info(url):
    res = requests.get(url)

    ids = re.findall('<h2>(.*?)</h2>',res.text,re.S)        #用户ID
    sexs = re.findall('<div class="articleGender(.*?)">',res.text,re.S)
    contents = re.findall('<div class="content">.*?<span>(.*?)</span>',res.text,re.S)
    laughs = re.findall('<span class="stats-vote"><i class="number">(\d+)</i>',res.text,re.S)
    comments = re.findall('<i class="number">(.*?)</i>',res.text,re.S)

    for id,sex,content,laugh,comment in zip(ids,sexs,contents,laughs,comments):
        info = {
            'id':id,
            'sex':judgment_sex(sex),                    #调用性别判断函数
            'content':content,
            'laugh':laugh,
            'comment':comment
        }
        info_lists.append(info)                          #获取数据,并append到列表中
    

if __name__ == '__main__':                              #主函数入口
    urls = ['https://www.qiushibaike.com/8hr/page/{}/'.format(str(i))for i in range(1,14)]
    for url in urls:
        get_info(url)                                    #循环调用获取爬虫信息函数
    for info_list in info_lists:
        f = open('C:/Users/Administrator/Desktop/糗事.txt','a+')
        #遍历列表，创建TXT文件
        try:
            f.write('ID:'+info_list['id']+'\n')
            f.write('性别:'+info_list['sex']+'\n')
            f.write('内容:'+info_list['content']+'\n')
            f.write('评论:'+info_list['laugh']+'\n')
            f.write('好评'+info_list['comment']+'\n\n')
            f.close()                                   #写入到文件中
        except UnicodeEncodeError:
            pass                                        #屏蔽掉错误编码