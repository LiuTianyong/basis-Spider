import time

time = time.ctime()
time = time.split(' ')[-2]
time = time.replace(':',',')
print(time)