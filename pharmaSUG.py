# -*- coding: utf-8 -*-
"""
Created on Thu May 23 19:21:57 2019

@author: zwn
"""

import os
import re
import time
import datetime
import random
import urllib
import urllib.request
import requests

# url_list =['https://lexjansen.com/cgi-bin/xsl_transform.php?x=phuse-us'
#            'https://lexjansen.com/cgi-bin/xsl_transform.php?x=sgf',
#            'https://lexjansen.com/cgi-bin/xsl_transform.php?x=css-us',
#            'https://lexjansen.com/cgi-bin/xsl_transform.php?x=pharmasug',
#            'https://lexjansen.com/cgi-bin/xsl_transform.php?x=pharmasug-cn',
#            'https://lexjansen.com/cgi-bin/xsl_transform.php?x=wuss',
#            'https://lexjansen.com/cgi-bin/xsl_transform.php?x=mwsug',
#            'https://lexjansen.com/cgi-bin/xsl_transform.php?x=scsug',
#            'https://lexjansen.com/cgi-bin/xsl_transform.php?x=sesug',
#            'https://lexjansen.com/cgi-bin/xsl_transform.php?x=phuse']

url_list =['https://lexjansen.com/cgi-bin/xsl_transform.php?x=pharmasug',
           'https://lexjansen.com/cgi-bin/xsl_transform.php?x=pharmasug-cn',
           'https://lexjansen.com/cgi-bin/xsl_transform.php?x=wuss',
           'https://lexjansen.com/cgi-bin/xsl_transform.php?x=mwsug',
           'https://lexjansen.com/cgi-bin/xsl_transform.php?x=scsug',
           'https://lexjansen.com/cgi-bin/xsl_transform.php?x=sesug',
           'https://lexjansen.com/cgi-bin/xsl_transform.php?x=phuse']

year_list = list(range(2015,2021))
year_list.reverse()

# setup
currentroot = os.getcwd()

try:
	os.mkdir('pharmaSUG')
except FileExistsError:
	pass
	
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'}

t1 = datetime.datetime.now()
print('开始时间:', t1.strftime('%Y-%m-%d %H:%M:%S'))

###############################################################################
#debug

#url = 'https://lexjansen.com/cgi-bin/xsl_transform.php?x=sgf2019'
#request = urllib.request.Request(url, headers=headers)
#response = urllib.request.urlopen(request)
#html = response.read().decode('utf-8')
#strings = []
#response = requests.get(url, headers=headers)
#response.encoding = 'utf-8'
#html = response.text
#reg = re.compile(r'http.{1,150}?pdf">.{1,300}?</a><br />', re.S)
#string = re.findall(reg, html)
#strings.extend(string)
###############################################################################


strings = []
for i in url_list:
    for j in year_list:
        url = i + str(j)
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        html = response.text
        reg = re.compile(r'http.{1,150}?pdf">.{1,300}?</a><br />', re.S)
        string = re.findall(reg, html)
        strings.extend(string)
    
urls = []
titles = []
for i in strings:
    urls.append(i[0:i.find('pdf')+3])
    s = r'[\\\/\:\*\?\"\<\>\|]'
    #s = r'[\u005C\u002f\u003a\u002a\u003f\u0022\u003c\u003e\u007c]'
    j = i[i.find('pdf')+5:-10]
    k = re.sub(s, '', j).strip()
    titles.append(k)
    
dic = dict(zip(urls, titles))  

num = 1
for url, title in dic.items():
    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        obj = response.read()
    except urllib.error.HTTPError as e:
        print('HTTPError', e.code)
    except urllib.error.URLError as e:
        print('URLError', e.reason)
    else:
        f = open('pharmaSUG/{}.pdf'.format(title), 'wb') 
        f.write(obj)
        num += 1
        time.sleep(random.randint(15,20))
        print('完成下载第{}个PDF文件: {}.pdf'.format(num-1, title))
        response.close()
        f.close()


# 开始时间
print('开始时间:', t1.strftime('%Y-%m-%d %H:%M:%S'))
# 结束时间
t2 = datetime.datetime.now()
print('结束时间:', t2.strftime('%Y-%m-%d %H:%M:%S'))
delta = t2 - t1

if delta.seconds > 3600:
    if t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] < t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：'
              + str(int(round(delta.seconds / 3600, 0))) + '时'
              + str(int(round(delta.seconds / 60, 0) % 60)) + '分'
              + str(delta.seconds % 60) + '秒')
    elif t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] == t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：'
              + str(int(round(delta.seconds / 3600, 0))) + '时'
              + str(int(round(delta.seconds / 60, 0) % 60)) + '分'
              + '0秒')
    elif t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] > t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：'
              + str(int(round(delta.seconds / 3600, 0))) + '时'
              + str(int(round(delta.seconds / 60, 0) % 60)-1) + '分'
              + str(delta.seconds % 60) + '秒')
        
elif delta.seconds > 60:
    if t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] < t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：' + str(int(round(delta.seconds / 60, 0))) + '分'
              + str(delta.seconds % 60) + '秒')
    elif t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] == t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：' + str(int(round(delta.seconds / 60, 0))) + '分'
              + '0秒')
    elif t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] > t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：' + str(int(round(delta.seconds / 60, 0))-1) + '分'
              + str(delta.seconds % 60) + '秒')

else:
    print('总共耗时：' + str(delta.seconds) + '秒')
