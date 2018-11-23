import requests


url = 'http://pic.sogou.com/pics?query=%D5%D4%C0%F6%D3%B1&mode=1&start=48&reqType=ajax&reqFrom=result&tn=0'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}

res = requests.get(url)
selector = res.json()
data = selector['items']
imgs = []

for i in data:
    imgs.append(i['simdata'])

l = 1
for i in imgs:
    if type(i) == list:
        for j in i:
            photo = requests.get(j[-1],headers=headers)
            fp = open('赵丽颖\\'+'{}'.format(l)+'赵丽颖.jpg','wb')
            fp.write(photo.content)
            fp.close()
            l += 1
    if l == 21:
        break



