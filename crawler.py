import requests
import chardet
from bs4 import BeautifulSoup
import pymongo
import urllib
import urllib.request
import time
import urllib.error
import socket
socket.setdefaulttimeout(20)  # 设置socket层的超时时间为20秒
client=pymongo.MongoClient()
db=client.Mydatabase
Company=db.Company
Person=db.Person
def Company_crawler():
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/60.0.3112.113 Safari/537.36",
        'Cookie': "your own cookie"
    }
    pre_url = "http://data.cfi.cn/cfidata.aspx?sortfd=&sortway=&curpage="
    post_url = "&fr=content&ndk=A0A1934A1939A1947A1952&xztj=&mystock="
    for i in range(1, 74):
        url = pre_url + str(i) + post_url
        data = requests.get(url, headers=headers).text
        soup = BeautifulSoup(data, "html.parser")
        table = soup.find_all("table", "table_data")
        for i in table:
            res = i.find_all('tr')[1:]

            for ind, tmp in enumerate(res):
                # print(ind,tmp)
                company_info = {}
                tds = tmp.find_all('td')
                company_info['代码'] = tds[0].find_all('a')[0].contents[0]
                company_info['证券简称'] = tds[1].find_all('a')[0].contents[0]
                company_info['公司名称'] = tds[2].contents[0]
                company_info['公司注册地址'] = tds[3].contents[0]
                company_info['公司注册地址邮箱'] = tds[4].contents[0]
                company_info['首次注册登陆地点'] = tds[5].contents[0]
                company_info['企业法人营业执照注册号'] = tds[6].contents[0]
                company_info['法人代表'] = tds[7].contents[0]
                company_info['总经理'] = tds[8].contents[0]
                Company.insert(company_info)

def Person_scrawler():
    headers={
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        'Cookie':"your own cookie"
    }
    url="http://www.cninfo.com.cn/cninfo-new/information/companylist"
    data=requests.get(url,headers).text
    soup=BeautifulSoup(data,'html.parser')
    #先爬到企业名称和代码，以及详细公司链接，再根据链接爬到高管页面，再提取高管信息。
    company_list=soup.find_all("ul","company-list")

    for company in company_list:


        li_list=company.find_all("li")
        for li in li_list:
            temp = li.find_all("a")[0]
            try:
                # print(temp["href"])
                # 找出高管页面
                code = temp['href'].split('?')[-1]
                # http://www.cninfo.com.cn/information/management/szmb000001.html
                url_new = "http://www.cninfo.com.cn/information/management/" + code + ".html"
                # data_new=requests.get(url_new,headers)
                uf=urllib.request.Request(url_new,headers=headers)




                fp = urllib.request.urlopen(uf)
                # print(fp.info())

                # #gb2312
                # print(data_new.encoding)

                soup_new = BeautifulSoup(fp.read().decode('gbk'), "html.parser")
                table_new = soup_new.find_all("div", "clear")[0]

                tr_list = table_new.find_all("tr")[1:]
                for tr in tr_list:
                    person = {}
                    listwords = temp.contents[0].split(' ')

                    person["代码"] = listwords[0]

                    person["证券简称"] = ''.join(listwords[1:])

                    info = tr.find_all("td")
                    print(info)
                    person["姓名"] = info[0].contents[0][:-3]
                    person["职务"] = info[1].contents[0][:-3]
                    person["出生年月"] = info[2].contents[0][:-3]
                    person["性别"] = info[3].contents[0][:-2]
                    person["学历"] = info[4].contents[0][:-2]
                    print(person)
                    print('\n')

                    Person.insert(person)
                fp.close()
            except urllib.error.URLError as e:
                print(e.reason)
            time.sleep(5)


if __name__=='__main__':
    Person_scrawler()
    # Company_crawler()
















