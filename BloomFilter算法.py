#url最优去重算法    布隆过滤器
#工作机制   采用多哈希函数共同工作解决原有 单个哈希函数碰撞问题
from pybloom import BloomFilter
from pybloom import ScalableBloomFilter

#BloomFilter
#布隆过滤器

#创建一个容量为1000   漏失为0.001的布隆过滤器
#静态指定容量
f = BloomFilter(capacity=1000 ,error_rate= 0.001)

print([f.add(x) for x in range(10)])
print(11 in f)
print(4 in f)
print('************************************')

#动态扩展容量
sbf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
count = 10000
for i in range(0,count):
    sbf.add(i)

print(10001 in sbf)
print(4 in sbf)

