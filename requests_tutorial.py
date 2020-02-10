import requests
import re

html = requests.get('http://exercise.kingname.info/exercise_requests_get.html')
print(html)
html_bytes = html.content
html_strs = html_bytes.decode('utf-8')
content = html_strs
title = re.findall('title>(.*?)</title', content, re.S)
p = re.findall('p>(.*?)</p', content, re.S)

ch_p = []
for each in p:
    ch_p.append(re.findall('[\u4e00-\u9fa5，]+', each, re.S))
print('title:', title[0])
print('p:\n', '\n'.join(p))
print('Chinese in p:\n', ch_p[0], '\n', ch_p[1])

data = {'name': 'jacky',
        'password': 'male'}
html_postdata = requests.post('http://exercise.kingname.info/exercise_requests_post', data=data)
html_postdata2 = requests.post('http://exercise.kingname.info/exercise_requests_post', json=data)
print(html_postdata.content.decode())
print(html_postdata2.content.decode())
