# Code based on Python 3.x
# _*_ coding: utf-8 _*_
# __Author: "jordan"

TOTAL_PAGE_NUMBER = 5  # PAGE_NUMBER: total number of pages，可进行修改

KEYWORDS = ['数据', '大数据']   # 需爬取的关键字可以自己添加或修改

# 爬取主要城市的记录
CITY_SELECT = ['489']        # 选取下面字典表中的某个城市的字典码
CITY_DICT = {'489': '全国',
        '530': '北京',
        '538': '上海',
        '765': '深圳',
        '763': '广州'}

# MONGO_URI = 'localhost'
# MONGO_DB = 'zhilian'
FILEPATH = 'result'
FILENAME = '+'.join(CITY_DICT[i] for i in CITY_SELECT) + '地区' + '+'.join(str(i) for i in KEYWORDS) + '岗位统计结果'
# 统计范围，不可编辑
RESULT_HEAD = ['地区', '公司名', '人员数', '公司性质', '学历要求', '职业类型', '岗位描述', '职位类别', '薪资', '福利', '发布时间', '工作经验', '岗位链接']
