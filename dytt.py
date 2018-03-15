import requests
import re
import os
url='http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=detail&fr=&sf=1&fmq=1447473655189_R&pv=&ic=0&nc=1&z=&se=&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E9%95%BF%E8%80%85%E8%9B%A4'
html = requests.get(url).text
urls = re.findall('"objURL":"(.*?)"', html)
if not os.path.isdir('C:\\Users\\wangz\\Desktop\\dytt'):
    os.mkdir('C:\\Users\\wangz\\Desktop\\dytt')

index = 1
for url in urls:
    print("Doading:",url)
    res=requests.get(url)
    filename = os.path.join('C:\\Users\\wangz\\Desktop\\dytt', str(index) + ".jpg")
    with open(filename, 'wb') as f:
        f.write(res.content)
        index += 1