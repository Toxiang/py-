from selenium import webdriver
from bs4 import BeautifulSoup
import time

allInfo = []
driver = webdriver.Chrome(executable_path="D:\py\chromedriver.exe")
def getInfo(info):
    bookInfo = []
    for book in info:
        # print(book.text)
        # print("----------------------------------")
        bookUrl = book.find_element_by_class_name("nbg").get_attribute('href')
        # print(bookUrl)
        imgUrl = book.find_element_by_xpath('.//img').get_attribute('src')
        # print(imgUrl)
        # 寻找class的两种写法
        bookName = book.find_element_by_class_name("pl2").text.strip()
        # print(bookName)
        bookSplit = book.find_element_by_xpath('.//p[@class="pl"]').text.strip()
        # print(bookSplit)
        bookRate = book.find_element_by_xpath('.//span[@class="rating_nums"]').text
        # print(bookRate)
        # 因为有些没有评价 所以跳过
        bookComment = None
        try:
            bookComment = book.find_element_by_xpath('.//span[@class="inq"]').text.strip()
            # print(bookComment)
        except:
            pass
        t = [bookUrl,imgUrl,bookName,bookSplit,bookRate,bookComment]
        bookInfo.append(t)
    return bookInfo


def douban(url):
    driver.get(url)
    driver.maximize_window()
    # getInfo()

    i = 10
    while(i>1):
        # time.sleep(1)
        i = i - 1
        info = driver.find_elements_by_class_name("item")
        allInfo.append(getInfo(info))
        # 找到 下一页的链接 进入下一页
        driver.find_element_by_xpath('//div[@class="paginator"]/span[@class="next"]/a').click()
    info = driver.find_elements_by_class_name("item")
    allInfo.append(getInfo(info))


if __name__ == '__main__':
    url = 'https://book.douban.com/top250?start=0'
    douban(url)
    driver.quit()