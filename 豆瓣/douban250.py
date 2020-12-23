from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


# 页面分析
# 一页有25条数据 共分成十页
# 每本书包含信息
# 书名
# 作者(部分包含译者) 出版社 出版年份 价格
# 评分
# 热评
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
AllInfo = []
# https://book.douban.com/top250?start=0 第一页
# https://book.douban.com/top250?start=25 第二页
# https://book.douban.com/top250?start=50 第三页
# 可发现规律 strar = (page-1)*25表示页面
def getAllUrl(url):
    #也可以从页面中获取所有页面url
    # 这个地方有个小坑 一定要写成headers = headers 否则可能报错418
    page = requests.get(url,headers=headers).text
    soup = BeautifulSoup(page,'lxml')
    # print(soup)
    List = soup.find(class_='paginator').find_all('a',href=True)
    urlList = []
    for i in List:
        urlList.append(i['href'])
    return urlList
# 初始表示第一页

# 得到每本书的info
def getBookInfo(book):

    td = book.find_all('td')
    # 书籍链接
    bookUrl = td[0].find('a',href=True)['href']
    # 图片链接
    imgUrl = td[0].find('img').get('src')
    # print(bookUrl,imgUrl)
    # 书名
    bookName = td[1].find('a').text.strip()
    # 图书信息混合 后面分割
    bookSplit = td[1].find(class_='pl').text.strip()
    # 图书评分
    bookRate = td[1].find(class_='rating_nums').text.strip()
    bookHotComment = None
    # 有些书没有评价 加判断 否则会报错
    if(td[1].find(class_='quote')!=None):
        bookHotComment = td[1].find(class_='quote').text.strip()
    # print(bookName,bookSplit,bookRate,bookHotComment)
    info = bookSplit.split('/')
    bookPrice = info[-1]
    bookDate = info[-2]
    bookPub = info[-3]
    bookAuthor = info[0]
    if(len(info)>4):
        for i in range(1,len(info)-3):
            bookAuthor = bookAuthor+'/'+info[i]
    info = [bookUrl,imgUrl,bookName,bookRate,bookHotComment,bookPrice,bookDate,bookPub,bookAuthor]
    return info



# 得到 当前页面信息 25本图书
def getPageInfo(url):
    page = requests.get(url,headers=headers).text
    soup = BeautifulSoup(page,'lxml')
    bookContent = soup.find(class_='indent').find_all('table')
    bookInfo = []
    for book in bookContent:
        # print(type(book))
        AllInfo.append(getBookInfo(book))
        # return
    # return bookInfo

def save():
    bookList = []
    for i in AllInfo:
        book = dict(zip(['链接','图片','书名','评分','热评','价格','出版日期','出版社','作者'],i))
        # print(book)
        bookList.append(book)
    df = pd.DataFrame(bookList)
    df.to_csv("豆瓣250.csv")


if __name__ == '__main__':
    # 初始url
    page =1
    initUrl = "https://book.douban.com/top250?start=0"

    """ Test url"""
    # AllInfo = getPageInfo(initUrl)
    pageUrl = getAllUrl(initUrl)
    pageUrl.pop(9) #去掉最后一个
    pageUrl.insert(0,initUrl)
    for url in pageUrl:
        getPageInfo(url)
    save()
    # print(pageUrl)