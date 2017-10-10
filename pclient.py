import re
from selenium import webdriver
from bs4 import BeautifulSoup
import subprocess
import os
import urllib
import copy
import time

#proxy
proxy_args = [
    '--proxy=localhost:8080',
    '--proxy-type=http',
    ]

#edit:this is the url you want to test~~~
main_url='http://you.163.com/act/static/cVu7GRWG0N.html'
#main_url = 'http://www.hdu.edu.cn/'
#main_url="http://172.16.227.128/other/"
#main_url='http://www.cnblogs.com/Silvia/archive/2012/06/15/2550691.html'
#main_url="http://hzwebmail.mail.163.com/js6/main.jsp?sid=yCNGUbYAasGnDYVPhTAAAyOOPIJZFusE&df=idc2email163#module=mbox.ListModule%7C%7B%22fid%22%3A1%2C%22order%22%3A%22date%22%2C%22desc%22%3Atrue%7D"
#main_url="https://baidu.com/"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#page diction
page={}
index=0
iter_num=1
keyword=[]
js_file=[]
version=1

#r is used for find the spacial string and solve it
r=re.compile(r'cesign_[0-9]*?_[0-9]*')

#global var,set proxy,disable cache


#edit,the path of chromdriver
chromedriver = '/home/cesign/sf/cd/chromedriver'
chome_options = webdriver.ChromeOptions()
chome_options.add_argument(('--proxy-server=http://' + 'localhost:8080'))
chome_options.add_argument("--disable-application-cache")
chome_options.add_argument("--disk-cache-size=0")

os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver, chrome_options=chome_options)

def iteration_get(url):
	global iter_num
	global r
	url=url.replace('&','*')+'&cesign='+str(iter_num)
	iter_num+=1
	if '?' not in main_url:
		strAddr=main_url+'?page=1&url='+url+'&init=false'
	else:
		strAddr=main_url+'&page=1&url='+url+'&init=false'
	driver.get(strAddr)
	time.sleep(1)
	soup=BeautifulSoup(driver.page_source,'html.parser')
	for each in soup.find_all(name='a'):

		if 'cesign' in str(each):
			rp=re.split(r'\/|\&|\?|\:',url.replace('*','&'))
			tmp=re.findall(r,each.get('href'))
			print each.get('href')
			#tmp=tmp.split('_')
			for tmp_it in tmp:
				tmp_it=str(tmp_it)
				tmp_it=tmp_it.split('_')
				#print str(tmp_it)+'~'+str(rp)+'~'+str(keyword)
				if rp[int(tmp_it[1])] not in keyword:
					keyword.append(rp[int(tmp_it[1])])
					print rp[int(tmp_it[1])]+'&'+tmp_it[2]

def js_iteration(url,page):
	global r
	global version
	page+=2
	global iter_num
	url=url.replace('&','*')+'&cesign='+str(iter_num)
	iter_num+=1
	#radom,page
	if '?' not in main_url:
		strAddr=main_url+'?page='+str(page)+'&url='+url+'&init=false'
	else:
		strAddr=main_url+'&page='+str(page)+'&url='+url+'&init=false'
	driver.get(strAddr)
	time.sleep(1)
	soup=BeautifulSoup(driver.page_source,'html.parser')
	for each in soup.find_all(name='a'):
		if 'cesign' in str(each):
			rp=re.split(r'\/|\&|\?|\:',url.replace('*','&'))
			tmp=re.findall(r,each.get('href'))
			#tmp=tmp.split('_')
			for tmp_it in tmp:
				tmp_it=str(tmp_it)
				tmp_it=tmp_it.split('_')

				if rp[int(tmp_it[1])] not in keyword:
					keyword.append(rp[int(tmp_it[1])])
					print rp[int(tmp_it[1])]+'&'+tmp_it[2]



def main(url):
	global keyword
	if '?' not in main_url:
		driver.get(main_url+'?page=1&init=true')
	else:
		driver.get(main_url+'&page=1&init=true')

	#Wait the page loaded completely
	time.sleep(1)

	#Save url
	i = 0
	old_url_save = {}
	furl = open('./c/url.txt','w')
	source = driver.page_source
	soup = BeautifulSoup(source,"html.parser")
	href = soup.find_all(name='a')

	for each in href:
	    furl.write(str(each.get('href'))+'\n')
	    old_url_save[i]=str(each.get('href'))
	    i+=1
	furl.close()
	#print old_url_save
	print '-'*20+'ORINGINAL URL'+'-'*20
	for i in range(len(old_url_save)):
		if old_url_save[i]!='':
			print old_url_save[i]

	#test url
	print '-'*20+'RESULT'+'-'*20
	print '[*] page:main.html'
	for j in range(len(old_url_save)):
		if old_url_save[j]!='':
			sta=False
			url_check=re.split(r'\/|\&|\?|\:',old_url_save[j])
			for m in url_check:
				#same formate urls are not necessary to test,so beside them
				if 'http' not in m and '.' not in m and '=' not in m and m != '':
					if m in keyword:
						sta=True
					else:
						sta=False
						break
			if not sta:
				iteration_get(old_url_save[j])

	#js_file_test
	src=soup.find_all(name='script')
	for i in src:
		if i.get('src') != None:

			js_file.append(os.path.basename(str(i.get('src'))).split('?')[0])
	for i in range(len(js_file)):
		print '[*] page:'+js_file[i]
		global keyword
		keyword=[]
		#except some js respon
		if 'jquery' not in js_file[i] and 'bootstrap' not in js_file[i]:
			for j in range(len(old_url_save)):
				if old_url_save[j]!='':
					js_iteration(old_url_save[j],i)

if __name__ == '__main__':
    main('test')

# about the result
# [*] page:test.js
# word&3 means that the url is related to the third word 'word' in the file test.js
