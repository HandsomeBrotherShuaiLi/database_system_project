import requests
from bs4 import BeautifulSoup
import re
import codecs
from contextlib import closing
import json
import pymongo
import gridfs
import os
import pymysql
client=pymongo.MongoClient('localhost',27017)
db=client.sense
data=db.data
imgput=gridfs.GridFS(db)


download_url="https://movie.douban.com/top250"
def download_page(url):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36'
    }
    data=requests.get(url,headers=headers).text
    return data
def parse_html(html):
    sp=BeautifulSoup(html,"html.parser")
    movielistsoup=sp.find('ol',attrs={'class':"grid_view"})
    movie_list=[]

    for movie in movielistsoup.find_all('li'):
        detail=movie.find('div',attrs={'class':'hd'})
        movie_name=detail.find('span',attrs={'class':'title'}).getText()
        movie_score=movie.find('span',attrs={'class':'rating_num'}).getText()
        movie_list.append(movie_name+movie_score)
    next_page=sp.find('span',attrs={'class':'next'}).find('a')
    if next_page:
        return movie_list,download_url+next_page['href']
    return movie_list,None
def getpic(data):
    pic_list=re.findall('src="http.+?.jpg"',data)
    return pic_list
def download_pic(url,name):
    rootpath="S:\\pycharm\\database_system_project\\pic\\"
    response=requests.get(url,stream=True)
    pic_type='.'+url.split('.')[-1]
    with closing(requests.get(url,stream=True)) as response:
        with open(rootpath+name+pic_type,'wb') as file:
            for data in response.iter_content(128):
                file.write(data)
if __name__=='__main__':
    url=download_url
    n=1
    # db=pymysql.connect('localhost','testuser','test123','TESTDB')
    # cursor=db.cursor()
    # cursor.execute('SELECT VERSION()')
    # data=cursor.fetchone()
    # print(data)
    # db.close()
    with codecs.open('movies','w',encoding='utf-8') as fp:
        while(url):
            html=download_page(url)
            picdata=getpic(html)
            index=0
            movies,url=parse_html(html)

            for picinfo in picdata:
                download_pic(picinfo[5:-1],'Top' + str(n) +'-'+ movies[index])
                src={'name':movies[index]}
                data.insert_one(src)
                print(movies[index]+'下载完毕')
                n+=1
                index+=1
            fp.write(u'\n'.join(movies))



