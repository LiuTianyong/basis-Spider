import re

a = 'xxIxxxxLovexx-x++5x454x5+--533xxPythonxx'
info = re.findall('xx(.*?)xx',a)
print(info)

b = 'one1two2three3'
info_1 = re.search('\d+',b)
print(info_1.group())

c = '123-4565-7895'
phone = re.sub('\D','',c)
print(phone)

c = 'one1two2three3'
info_2 = re.findall('\d+',c)
print(info_2)