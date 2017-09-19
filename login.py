# -*- coding:utf-8 -*-
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import sys
'''
页面登录脚本，给定url，用户名和密码，登录页面
'''

reload(sys)
sys.setdefaultencoding('utf8')

# 用户资料
userinfo = {
    'username':'username',
    'password':'passwd'
}

# 输入框关键词
username = ['username','name','email','user','phone','phoneNumber']
password = ['passwd','password','pass']

# 登录按钮
login = ['登录',"login","Login"]

chromedriver = '/home/cesign/sf/cd/chromedriver'
chome_options = webdriver.ChromeOptions()
chome_options.add_argument("--disable-application-cache")
chome_options.add_argument("--disk-cache-size=0")
driver = webdriver.Chrome(chromedriver, chrome_options=chome_options)

def sendData(usernameid,passwordid,submitid):
    global userinfo
    print userinfo['username']
    print userinfo['password']
    driver.find_element_by_id(usernameid).send_keys(userinfo['username'])
    driver.find_element_by_id(passwordid).send_keys(userinfo['password']);
    time.sleep(6)
    # 现在的问题是id重复，导致的问题
    driver.find_element_by_id(submitid).submit()

def main(url):
    global driver
    usernameid = ''
    passwordid = ''
    submitid = ''
    formid = ''
    driver.get(url)
    source_code = BeautifulSoup(driver.page_source,'html.parser')
    form_code = source_code.find_all('form')[0]
    formid = form_code.get('id')
    print formid
    form_code = str(form_code)
    form_code = BeautifulSoup(form_code,'html.parser')
    input_find = form_code.find_all('input')
    for i in input_find:
        if i.get('type') != 'hidden' and i.get('name') in username:
            usernameid = i.get('id')
        if i.get('type') != 'hiddne' and i.get('name') in password:
            passwordid = i.get('id')
        # if i.get('value') in login and i.get('type') != 'hidden':
        #      submitid = i.get('id')
    # print submitid
    # id找到，接下来sendtext和submit数据
    sendData(usernameid,passwordid,formid)

# 测试部分
url="http://cas.hdu.edu.cn/cas/login"
main(url)
