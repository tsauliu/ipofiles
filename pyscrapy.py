#-*-coding:utf-8 -*-
import sys
import pprint
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
urldict={}
import os
try:
    os.mkdir('./output')
except:
    pass

#从巨潮资讯解析出pdf的真实下载地址
f=open('stkcd.csv','r')
fout=open('./output/urls.csv','w')
for line in f:
    stkcd = str(line[:6])
    # 这一行把“招股说明书”换成　“年报”　“半年报”　之类的，即可批量下载其他的公告
    response=requests.get('http://www.cninfo.com.cn/cninfo-new/fulltextSearch/full?searchkey='+stkcd+'+招股说明书&sdate=&edate=&isfulltext=false&sortName=nothing&sortType=desc&pageNum=1')
    dict=response.json()
    for i in dict['announcements']:
        if '摘要'.decode('utf-8') not in i['announcementTitle']:
            print i['announcementTitle']
            url='http://www.cninfo.com.cn/'+i['adjunctUrl']
            print url
            secname=i['secName']
            date=i['adjunctUrl'][10:20]
            urldict.update({stkcd+'-'+secname+'-'+date:url})
            csvtowrite=stkcd+','+secname+','+date+','+url+'\n'
            fout.write(csvtowrite.encode('gbk'))
pprint.pprint(urldict)
fout.close()

#根据解析出的pdf地址下载到output，并重命名成有规律的文件
import urllib2
for name in urldict:
    url=urldict[name]
    response = urllib2.urlopen(url)
    file = open('./output/'+name+".pdf", 'wb')
    file.write(response.read())
    file.close()
    print name
