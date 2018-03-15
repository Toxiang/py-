import requests
import re
n=1
url='https://www.qisuu.com/soft/sort01/index_1.html'
html=requests.get(url).text
#print(html)
novel_list=re.findall('<a href="(.*?)"><img src=".*?" onerror="this.src=.*?">.*?全集</a>',html)
#print(novel_list[0])
for i in novel_list:
    novel_url='https://www.qisuu.com'+i
    html_novel=requests.get(novel_url)
    html_novel.encoding='utf-8'
 #   print(html_novel.text)
    read_novel=re.findall('<a class="downButton" href=\'(.*?)\' title=".*?在线阅读">在线阅读</a>',html_novel.text)
    #print(read_novel)
    for j in read_novel:
        novel_list_url='https://www.qisuu.com/'+j
        novel_=requests.get(novel_list_url)
        novel_.encoding='utf-8'
        list=re.findall(' <li><a href=".*?">(.*?)</a></li>',novel_.text)
       # print(list)
        title=re.findall('<h1>(.*?)</h1>',novel_.text)
        print(title)
        print("正在爬取第"+str(n)+"本章节")
        n=n+1
        with open('C:\\Users\\wangz\\Desktop\\qsw\\novel2.txt','a') as ff:
            ff.write(title[0] + '\n')
            for k in list:
                ff.write(k+'\t')
            ff.write('\n')