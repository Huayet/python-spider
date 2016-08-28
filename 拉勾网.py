#coding=utf-8

import requests
import json
# import xlwt3 py3版本用这个
import xlwt
import time
import random
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

def get_job(keyword,pagenum,city):
    js_data=requests.get('http://www.lagou.com/jobs/positionAjax.json?px=new&city=%s&kd=%s&pn=%s&'%(city,keyword,pagenum),headers=headers).text
    data=json.loads(js_data)
    #开始层级读取json内容
    data=data['content']
    data=data['positionResult']
    data=data['result']
    jobs=[]
    for item in data:
        job={}
        job['positionName']=item['positionName']
        job['company']=item['companyShortName']
        job['salary']=item.get('salary')
        job['workYear']=item['workYear']
        job['education']=item['education']
        job['industryField']=item['industryField']
        job['companySize']=item['companySize']
        job['createTime']=item['createTime']
        if None!=item['district']:
            district=item['district']
        else:
            district='      '
        job['city']=item['city']+district
        job['financeStage']=item['financeStage']
        job['createTime']=item['createTime']
        jobs.append(job)
        #控制台输出信息
        print item['createTime']+'   '+job['city']+'   '+item['companyFullName']
    return jobs

def write2excel():
    excel=xlwt.Workbook()
    sheet=excel.add_sheet('sheet')
    count=0
    labels=['createTime','positionName','company','salary','workYear','education','industryField','companySize','city','financeStage']
    page=1
    while page<300:
        jobs=get_job('',page,'北京')
        # try:
        #     jobs=get_job('',page,'北京')
        # except:
        #     time.sleep(5)
        #     continue
        for job in jobs:
            num=0
            for i in labels:
                sheet.write(count,num,job[i])
                num+=1
            count+=1
        print('---------- Completed Page:'+str(page)+',Totle:'+str(count))
        page+=1
        time.sleep(random.randint(4, 7))#生成的随机数n: 1 <= n <= 10
        excel.save('jobs.xls')

def write2txt():
    f=open('job.txt','a')
    page=1
    count=0
    while page<300:
        try:
            jobs=get_job('',page,'北京')
        except:
            time.sleep(random.randint(4, 7))#生成的随机数n: 5 <= n <= 8
            continue
        for job in jobs:
            count+=1
            f.write(str(job)+'\n')
        print(page,count)
        page+=1
        time.sleep(2)
    f.close()

# write2txt()
write2excel()
