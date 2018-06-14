import json
import pandas as pd
import pymongo
import time
client=pymongo.MongoClient()
db=client.Mydatabase
Company=db.Company
Person=db.Person
# MR=db.MR
SPO=db.SPO
def process():
    """
    process json data and rebuild mongoDb
    manage->merge the two dataframe

    :return:
    """
    f = open("S:\kGraph\R+MySQL\items.json", encoding='utf-8')

    data = json.load(f)
    f.close()
    pa_company=pd.DataFrame(data)
    # for i in data:
    #     Company.insert(i)

    f=open("S:\kGraph\R+MySQL\persons.json", encoding='utf-8-sig')
    data=json.load(f)
    f.close()
    for i in data:
        i["代码"]=i["代码"][-6:]
        # Person.insert(i)
    pa_person=pd.DataFrame(data)

    manage=pd.merge(pa_company,pa_person,how='inner',on="代码")
    manage.to_csv("manage1.csv")
    manage2=pd.merge(pa_company,pa_person,how='outer',on="代码")
    manage2.to_csv('manage2.csv')

def spo():
    """
    spo-> subject,property and relationship


    :return:
    """
    #inner_join
    raw_data=pd.read_csv("manage1.csv").drop(["Unnamed: 0"],axis=1)
    companyset = set()
    pro = ["代码","公司注册地址", "公司注册地址邮箱", "总经理", "法人代表", "注册号", "证券简称", "首次注册登记地点"]
    for i in raw_data.index:
        # print(raw_data.iloc[i])
        # MR.insert(raw_data.iloc[i])
        tempmanager={}
        tempmanager['sub']=raw_data.iloc[i]['公司名称']
        tempmanager["prop"]="高管"
        tempmanager["obj"]=raw_data.iloc[i]["姓名"]
        tempmanager["type"]="relation"
        tempmanager["updata_time"]=time.asctime( time.localtime(time.time()) )
        # print(tempmanager)
        SPO.insert(tempmanager)


        if raw_data.iloc[i]["公司名称"] in companyset:
            pass

        else:
            for p in pro:
                company = {}
                company["sub"] = raw_data.iloc[i]['公司名称']
                company["prop"] =p
                company["obj"] = str(raw_data.iloc[i][p])
                company['type'] = "property"
                company["updata_time"] = time.asctime(time.localtime(time.time()))
                # print(company)
                SPO.insert(company)
        companyset.add(raw_data.iloc[i]['公司名称'])

if __name__=="__main__":
    spo()
    # process()

























