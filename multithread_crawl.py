from multiprocessing.dummy import Pool;
import requests
import time

# original:
for i in range(10):
    print(i ** i)


# multithread:
def cal_power2(num):
    return num ** num


pool = Pool(3)
num = [n for n in range(10)]
result = pool.map(cal_power2, num)
print(result)


# 爬取百度首页例子：
def query(url):
    requests.get(url)


list = []
for i in range(100):
    list.append('https://www.baidu.com')

start = time.time()
for i in range(100):
    query('https://www.baidu.com')
end = time.time()
print('单线程爬取百度，耗时：', end - start)

start = time.time()
pool = Pool(5)
pool.map(query, list)
end = time.time()
print('五线程爬取百度，耗时：', end - start)
