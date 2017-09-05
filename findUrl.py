# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
#import urllib
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')  


'''
脚本存在问题：
(1)性能存在很大的问题，一个页面存在的url一样，但每个也要请求一次，会造成资源的浪费
(2)如果存在动态url，必须有时间载入，也会造成性能问题
'''

#global val
urls = {}
totalUrls = []
deep = 0
cedUrls = []
outLink = ['javascript:;','/']

#Open the page without img
SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
driver = webdriver.PhantomJS(service_args=SERVICE_ARGS, executable_path='/home/cesign/sf/pj/bin/phantomjs')

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
		driver.get(startUrl)
		cedUrls.append(startUrl)
		# time.sleep(1)
		soup = BeautifulSoup(driver.page_source,"html.parser")
		#print driver.page_source
		for i in soup.find_all('a'):
			i = i.get('href')
			# print i
			# solve: a/b/c; a/b/c/
			if i != None and i != '':
				if i[0] == '/':
					if len(i) >= 2:
						if i[1] == '/':
							i = 'http:'+i
						else:
							i = otherAr+i							
				if i[0] == '.':
					i = re.findall(r'^[^?]*/',startUrl)[0]+i[2:]
				elif 'http' and ':' not in i:
					i = re.findall(r'^[^?]*/',startUrl)[0]+i
				if i[-1] == '/':
					i = i[:-1]
				#print i
				if i not in totalUrls:
					if not urls.has_key(de):
						urls[de] = []
					if i not in outLink and '#' not in i and re.findall(r'^http',i):
						if domain in re.findall(r'^[^?]*/',i)[0]:
							if i not in urls[de]:
								print i
								urls[de].append(i)
								totalUrls.append(i)
		if urls.has_key(de):
			for i in urls[de]:
				findUrls(i,de+1,domain, otherAr)

def main():
	global deep
	global totalUrls
	theDomain = 'bilibili.com'
	theStartRe = 'https://www.bilibili.com'
	print '[*] Trying to find urls....... Maybe it will take a lot of time...'
	findUrls("https://www.bilibili.com", deep, theDomain, theStartRe)
	#write the urls into file
	f = open('urls.txt','w')
	for i in totalUrls:
		f.write(i+'\n')
		#print i
	print '[*] Fninish!!!'
main()
driver.quit()