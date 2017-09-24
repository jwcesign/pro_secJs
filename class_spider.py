# -*-coding:utf-8-*-
import requests
import re
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import sys

'''
发现问题：网站的cookie与user-agent相关连，必须一一对应; 初始时一个cookie只能爬取一定的资料，必须更新;
'''
reload(sys)
sys.setdefaultencoding('utf8')

# 变量
urlMain = 'http://www.cnvd.org.cn'
url_be = 'http://www.cnvd.org.cn/flaw/typeResult?max=100&offset='
url_en = '&typeId=29'
# 获取信息量数, 没有应用
number_get = 30

# 通过无头游览器获取cookie,以待后面的应用
chromedriver = '/home/cesign/sf/cd/chromedriver'
chome_options = webdriver.ChromeOptions()
# chome_options.add_argument(('--proxy-server=' + 'localhost:8080'))
# 设置无头模式, 但无头模式的头不知道怎么取出： solved
chome_options.add_argument("--headless")
# 初始化游览器
driver = webdriver.Chrome(chromedriver, chrome_options=chome_options)
driver.set_page_load_timeout(5)
driver.set_script_timeout(5)
driver.get(urlMain)
# 获取到cookie
cookies = driver.get_cookies()
cookies_save=''
for i in cookies:
    cookies_save += i['name']+'='+i['value']+'; '

cookies_save = str(cookies_save[:-2])
# print cookies_save

def refCookie(page_code):
    global headers
    global driver
    global urlMain
    global cookies_save
    if len(page_code) < 100:
        driver.delete_all_cookies()
        driver.get(urlMain)
        cookies = driver.get_cookies()
        cookies_save = ''
        for i in cookies:
            cookies_save += i['name']+'='+i['value']+'; '


# 循环获取资料
def start():
    for i in range(0, 5000):
        headers = {
        'Host': 'www.cnvd.org.cn',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/58.0.3029.81 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': cookies_save}
        r = requests.get(url_be+str(i*100)+url_en, headers=headers)
        source_code = BeautifulSoup(r.content,'html.parser')
        # print source_code
        a_tag = source_code.find_all('a')
        if len(r.content) > 0 and 'CNVD' not in str(a_tag):
            print '[*] Over...'
            break;
        for i in a_tag:
            if 'type' not in i.get('href'):
                # 执行详细信息寻找
                tar = i.get('href')
                rs = requests.get(urlMain+tar,headers=headers)
                page = BeautifulSoup(rs.content,'html.parser')
                print '~'*30
                print '漏洞名称:'+page.h1.string
                td_tag = page.find_all('td')
                count = 1
                str_fi = ''
                for i in td_tag:
                    if count <= 14:
                        s = i.text
                        if s != None:
                            s = s.replace('\r','').replace(' ',' ').replace('\t','').replace('\n','')
                            if count%2 != 0:
                                str_fi += s
                            else:
                                str_fi += ':'+s
                                print str_fi
                                str_fi = ''
                            count += 1
        # 解决一个cookie只能请求有效次数的限制
        refCookie(r.content)
def main():
    start()

if __name__ == '__main__':
    main()
driver.quit()
