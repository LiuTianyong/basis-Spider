import csv

fp = open('C://Users/Administrator/Desktop/练习.csv','wt',newline='',encoding='UTF-8')
writer = csv.writer(fp)
writer.writerow(('我','书','shjdkko'))
fp.close()