# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
# import urllib
import sys
import os
import requests

reload(sys)
sys.setdefaultencoding('utf8')

'''
脚本存在问题：
(1)性能存在很大的问题，一个页面存在的url一样，但每个也要请求一次，会造成资源的浪费
(2)如果存在动态url，必须有时间载入，也会造成性能问题
'''

# global val
urls = {}
totalUrls = []
deep = 0
cedUrls = []
outLink = ['javascript:;', '/']

# Open the page without img
SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
driver = webdriver.PhantomJS(service_args=SERVICE_ARGS, executable_path='/home/cesign/sf/pj/bin/phantomjs')
driver.set_page_load_timeout(5)
driver.set_script_timeout(5)

def findUrls(startUrl, de, domain, otherAr):
    global outLink
    global urls
    global cedUrls
    global totalUrls
    if startUrl[-1] == '/':
        startUrl = startUrl[:-1]
    if de == 0:
        print startUrl
        urls[de] = []
        urls[de].append(startUrl)
        totalUrls.append(startUrl)
        de += 1
    if startUrl not in cedUrls:
        # 解决某些页面不能加载问题
        try:
            driver.get(startUrl)
            # time.sleep(1)
            soup = BeautifulSoup(driver.page_source, "html.parser")
        except:
            soup = BeautifulSoup('', "html.parser")
        cedUrls.append(startUrl)
        # print driver.page_source
        for i in soup.find_all('a'):
            i = i.get('href')
            # print i
            # solve: a/b/c; a/b/c/
            if i != None and i != '':
                # 解决http与https的问题 http://c.com, https://a.com
                if 'https' in otherAr:
                    i = i.replace('http:','https:')
                if i[0] == '/':
                    if len(i) >= 2:
                        if i[1] == '/':
                            if 'https' in otherAr:
                                i = 'https:' + i
                            else:
                                i = 'http:'+i
                        else:
                            i = otherAr + i
                if i[0] == '.':
                    if startUrl.count('/') == 2:
                        if startUrl[-1] != '/':
                            startUrl_b = startUrl+'/'
                    else:
                        startUrl_b = startUrl
                    i = re.findall(r'^[^?]*/', startUrl_b)[0] + i[2:]
                elif 'http' and ':' not in i:
                    if startUrl.count('/') == 2:
                        if startUrl[-1] != '/':
                            startUrl_b = startUrl+'/'
                    else:
                        startUrl_b = startUrl
                    i = re.findall(r'^[^?]*/', startUrl_b)[0] + i
                if i[-1] == '/':
                    i = i[:-1]
                if i[-1] == '/':
                    i = i[:-1]
                if i not in totalUrls:
                    if not urls.has_key(de):
                        urls[de] = []
                    if i not in outLink and '#' not in i and re.findall(r'^http', i):
                        if domain in re.findall(r'^[^?]*/', i)[0]:
                            if i not in urls[de]:
                                print i
                                urls[de].append(i)
                                totalUrls.append(i)
        if urls.has_key(de):
            for i in urls[de]:
                findUrls(i, de + 1, domain, otherAr)

def findDyUrls(url):
    # print url
    # 没有动态url的请求
    try:
        r = requests.get(url)
        # print '~~~~~~'
        source_basic = BeautifulSoup(r.text,"html.parser")
        url_basic = source_basic.find_all('a')
    except:
        return 0
    # 含有动态url的请求
    try:
        driver.get(url)
        source_contain = BeautifulSoup(driver.page_source,"html.parser")
        url_all = source_contain.find_all('a')
    except:
        return  0
    if url_all != url_basic:
        return 1
    else:
        return 0

def main(url):
    global deep
    global totalUrls
    # 同域名，不爬取子域名
    theDomain = url.replace('http://','').replace('https://','')
    theStartRe = url
    print '[*] Trying to find urls....... Maybe it will take a lot of time...'
    findUrls(url, deep, theDomain, theStartRe)
    # 把爬取到的url写入文件
    f = open('urls.txt', 'w')
    for i in totalUrls:
        f.write(i + '\n')
    # print i
    f.close()
    print '[*] Fninish!!!'
    # 寻找每个页面的动态url
    print "[*] start check...the following urls have..."
    f = open('urls.txt','r')
    line = f.readline()
    while (line):
        line = line.replace('\n','')
        if findDyUrls(line):
            print '[*] '+line
        line = f.readline()
    f.close()


# Testing part
url = "http://172.16.227.128/"
main(url)
driver.quit()
