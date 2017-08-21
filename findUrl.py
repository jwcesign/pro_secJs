# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import time
#import urllib


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

def findUrls(startUrl, de, domain):
	global outLink
	global urls
	global cedUrls
	global totalUrls
	if de == 0:
		urls[de] = []
		urls[de].append(startUrl)
		totalUrls.append(startUrl)
		de += 1
	if startUrl not in cedUrls:
		driver.get(startUrl)
		cedUrls.append(startUrl)
		#time.sleep(0.5)
		soup = BeautifulSoup(driver.page_source,"html.parser")
		#print driver.page_source
		for i in soup.find_all('a'):
			i = i.get('href')
			#print i
			if not urls.has_key(de) and i not in totalUrls:
				urls[de] = []
			if i is not None and i not in outLink and '#' not in i:
				if 'http' in i:
					if domain in i and urls.has_key(de):
						if i not in urls[de] and i not in totalUrls:
							print i
							urls[de].append(i)
							totalUrls.append(i)
				else:
					if i != '':
						if i[0] == '/':
							i = 'http://jwcesign.studio'+i
							#print i
							if domain in i and urls.has_key(de):
								if i not in urls[de] and i not in totalUrls:
									print i
									urls[de].append(i)
									totalUrls.append(i)
					else:
						if i != '':
							mainUrl = re.find_all(r'.*\/',i)[0]
							i = mainUrl+i
							#print i
							if domain in i and urls.has_key(de):
								if i not in urls[de] and i not in totalUrls:
									print i
									urls[de].append(i)
									totalUrls.append(i)
		if urls.has_key(de):
			for i in urls[de]:
				findUrls(i,de+1,domain)

def main():
	global deep
	theDomain = 'jwcesign.studio'
	findUrls("http://jwcesign.studio/", deep, theDomain)

main()
driver.quit()