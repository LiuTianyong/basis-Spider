import requests
# from lxml import etree
import time
import re
import requests
from bs4 import BeautifulSoup
from zhilian_config import *
import xlwt
import xlrd
import os
import matplotlib.pyplot as plt

def get_html_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    print('url:----------', url)
    response = requests.get(url, headers=headers).text
    return response

# 1.获取职位标签
def get_job_tag(starturl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    response = requests.get(starturl, headers=headers).text
    # print(response)
    # 解析源码
    # HTML = etree.HTML(response)

    soup = BeautifulSoup(response, 'html.parser')
    body = soup.body
    i = 0
    job_tag_links = soup.find('div', {'class': 'zp-jobNavigater-pop-list'}).find_all('a')
    job_tag = {}
    for job_tag_link in job_tag_links:
        job_tag[i] = job_tag_link.string
    return job_tag

def write_txt_file(path, txt, newlineflag):

    # print('newlonefalg:', newlineflag)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(txt + newlineflag)

def get_job_detail(html):
    requirement = ''
    soup = BeautifulSoup(get_html_info(html), 'html.parser')
    requirement_pre = soup.body.find('div', {'class': 'terminalpage-main clearfix'})
    print('tab-inner-cont:---------------\n', requirement_pre.find('div', {'class': 'tab-inner-cont'}))
    start_colect_flag = 0

    print(requirement_pre.find('div', {'class': 'tab-inner-cont'}).descendants)
    for child in requirement_pre.find('div', {'class': 'tab-inner-cont'}).find_all('p'):
        print('child:---', child.get_text())

        child_text = child.get_text().strip()
        # 碰到以下标签，设置标志位为1，开始提取其后所有标签
        if (child_text == '任职资格：') | (child_text == '任职要求') | (child_text == '素质要求'):
            start_colect_flag = 1
        # 标志位为1，开始提取内容
        if start_colect_flag == 1:
            # 去掉span标签内的'-'和空格
            requirement += child.get_text().replace('-', '').strip()
        # 碰到以下标签，设置标志位为0，其后所有标签将不在提取范围
        if (child_text == '岗位职责') | (child_text == '职位描述') | (child_text == '福利待遇') | (child_text == '工作地址'):
            start_colect_flag = 0
    return {'requirement': requirement}

# 获取职位信息
def get_job_info(infourl, start, city, kw):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    info_html = requests.get(infourl.format(start, city, kw), headers=headers).json()
    job_dict = {}

    for i in info_html['data']['results']:
        # 如果明细链接为空，跳过该条数据
        if i['positionURL'] == '':
            continue
        job_dict['city'] = i['city']['items'][0]['name']
        job_dict['company_name'] = i['company']['name']
        job_dict['company_size'] = i['company']['size']['name']
        job_dict['companyType'] = i['company']['type']['name']
        job_dict['eduLevel'] = i['eduLevel']['name']
        job_dict['emplType'] = i['emplType']
        job_dict['jobname'] = i['jobName']
        job_dict['jobType'] = i['jobType']['display']
        job_dict['salary'] = i['salary']
        job_dict['welfare'] = i['welfare']
        job_dict['updateDate'] = i['updateDate']
        job_dict['workingExp'] = i['workingExp']['name']
        job_dict['positionURL'] = i['positionURL']
        requires = get_job_detail(job_dict['positionURL']).get('requirement')

        write_txt_file(os.path.join(FILEPATH, FILENAME + '-requirements.txt'), requires, '')

    return info_html['data']['numFound']


# 过滤重复数据
companyList = []
jobNameList = []


# 读取.txt文件内容写入.xlsx
def writeintoxlsx(filename):
    # 打开文件
    fo = open(filename, 'r', encoding="utf-8")  # 读的方式打开txt文件
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)

    print("文件名: ", fo.name)
    rownum = 0
    rowdata = {}
    # 写入表头信息
    for i in range(len(RESULT_HEAD)):
        booksheet.write(rownum, i, RESULT_HEAD[i])
    rownum += 1
    # 循环读取每一行数据，并写入xls文件
    for line in fo:
        rowdata = line.split('::')
        for i in range(len(rowdata)):
            booksheet.write(rownum, i, rowdata[i])
        rownum += 1

    fo.close()
    workbook.save(os.path.join(FILEPATH, FILENAME + '.xls'))


        # 主函数
if __name__ == '__main__':



        #  一.请求首页

        # starturl = 'https://www.zhaopin.com/'
        # 获取职位标签-获取主页所有职位标签
        # job_tag_list = get_job_tag(starturl)
        # 获取职位标签-获取参数中设置的职位
        job_tag_list = KEYWORDS
        print('job_tag_list :' % job_tag_list)


         # 二.获取职位详细列表页面

        # 删除同名文件
        if os.path.exists(os.path.join(FILEPATH, FILENAME + '.txt')):
            os.remove(os.path.join(FILEPATH, FILENAME + '.txt'))

        if os.path.exists(os.path.join(FILEPATH, FILENAME + '-requirements.txt')):
            os.remove(os.path.join(FILEPATH, FILENAME + '-requirements.txt'))

        for city_select in CITY_SELECT:
            # 初始化分页参数
            start = 0
            page = 1
            while True:
                infourl = 'https://fe-api.zhaopin.com/c/i/sou?start={0}pageSize=60&cityId={1}&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={2}&kt=3'
                numFound = get_job_info(infourl, start, city_select, '+'.join(str(i) for i in job_tag_list))
                print('第{0}页'.format(page))
                # if start < numFound:
                if page < TOTAL_PAGE_NUMBER:
                    start += 60
                    page += 1
                    time.sleep(5)
                else:
                    break
