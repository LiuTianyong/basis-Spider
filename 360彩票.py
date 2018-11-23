import requests
import re
from lxml import etree

url = 'https://chart.cp.360.cn/zst/ssccq?lotId=255401&chartType=dww5&spanType=1&span=3&r=0.5845432204038099#roll_132'

res = requests.get(url)
selector = etree.HTML(res.text)

data = re.findall("<span class='sum'>(\d+)<strong class='num'>(\d+)</strong></span></strong></td>",res.text,re.S)

data_ = re.findall("<td class='tdbg_1' >(\d+)-(\d+)</td>",res.text)
print(data_)