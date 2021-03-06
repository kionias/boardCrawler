#!/usr/bin/python3

# 기본 사용법 (pip install beautifulsoup4)
from bs4 import BeautifulSoup
# from 모듈이름 import 클래스 이름
import urllib.request as req
import pandas as pd
import time

info=pd.DataFrame()
accum=pd.DataFrame()

for i in range(0,10):
    
    url = "https://www.clien.net/service/group/community?&od=T31&po=" + str(i)
    print(url)
    
    res = req.urlopen(url) #소스를 res로 넣는다
    soup = BeautifulSoup(res, "html.parser", from_encoding='utf-8')

    recommend = soup.select("div.list_content > div > div.list_symph > span")
    category = soup.select("div > div.list_title > a > span.shortname.fixed")
    title = soup.select("div > div.list_title > a > span.subject_fixed")
    reply = soup.select("div.list_content > div > div.list_title > a")
    writer = soup.select(" div.list_content > div > div.list_author")
    viewCnt = soup.select("div.list_content > div > div.list_hit > span ")
    dateTime =soup.select("div.list_content > div > div.list_time > span")
    docNo = soup.select("div.list_content > div > div.list_title > a.list_subject")
    photoyn = soup.select("div.list_content > div > div.list_title")


    recList =[]
    catList =[]
    titList =[]
    repList =[]
    wriList =[]
    viewList =[]
    datList =[]
    docList = []
    phoList = []

    #print("soup : {}".format(soup) )
    #print("recommend : {}".format(recommend) )
    
    # 가끔 게시물이 30개가 아닌경우가 있음
    length=len(recommend)

    for ind in range(length):
        rec = recommend[ind].text
        cat = category[ind].text
        tit = title[ind].text      
        view = viewCnt[ind].text
        dat = dateTime[ind].text.split("\t")[13].rstrip('\n')
        doc = docNo[ind]["href"].split("/")[4].split("?")[0]
        
        # if there's photo in article, also class "icon"
        if len(str(photoyn[0]).split("icon"))==2:
            pho = "Y"
        else:
            pho = "N"
        
        # if there's no reply, no data
        try:
            int(reply[ind].text)
            rep = int(reply[ind].text)
        except:
            rep = 0

        # if someone's nickname is image
        
        if len(writer[ind].text.split("\n")[3]) == 0:
            wri = str(writer[ind]).split('img alt="')[1].split('"')[0]
        else:
            wri = writer[ind].text.split("\n")[3]

        recList.append(rec)
        catList.append(cat)
        titList.append(tit)
        repList.append(rep)
        wriList.append(wri)
        viewList.append(view)
        datList.append(dat)
        docList.append(doc)
        phoList.append(pho)

    # list into dataframe
    info = pd.DataFrame(columns=['추천수'],data = recList)
    info['게시판'] = catList
    info['제목'] = titList
    info['리플수'] = repList
    info['아이디'] = wriList
    info['조회수'] = viewList
    info['날짜'] = datList
    info['문서번호'] = docList
    info['사진유무'] = phoList

   
    accum = pd.concat([accum,info])
    info =pd.DataFrame()
    
    time.sleep(0.3)
    
accum.reset_index(inplace = True)
accum.to_csv('./clien.csv')