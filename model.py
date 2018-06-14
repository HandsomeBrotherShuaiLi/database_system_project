import pymongo
import networkx as nx

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

client=pymongo.MongoClient()
db=client.Mydatabase
Company=db.Company
Person=db.Person
SPO=db.SPO
def search_company_fullname(input):



    res=SPO.find({'sub':input})
    if res==None:
        return 0,None
    G=nx.Graph()
    H = nx.Graph()
    G.add_node(input)
    H.add_node(input)
    list={}
    list2={}
    Dir=[]
    for i in res:
        if i['prop']!='高管':
            G.add_node(i['obj'])
            G.add_edge(input, i['obj'], weight=0.5)

            list.update({(input, i['obj']): i['prop']})
        else:
            G.add_node(i['obj'])
            G.add_edge(input, i['obj'], weight=0.5)

            H.add_node(i['obj'])
            H.add_edge(input, i['obj'], weight=0.5)

            list.update({(input, i['obj']): i['prop']})
            list2.update({(input, i['obj']): i['prop']})
            attr=Person.find({'姓名':i['obj']})[0]
            for j in attr.keys():
                if j=="姓名" or j=="_id" or j=="代码" or j=="性别" or j=="学历" or j=="出生年月":
                    pass
                else:
                    H.add_node(attr[j])
                    H.add_edge(i['obj'],attr[j],weight=0.5)
                    list2.update({(i['obj'],attr[j]):j})
    fig = plt.figure(input + "关系图")
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='pink')
    nx.draw_networkx_edges(G, pos, edge_color='red')
    nx.draw_networkx_labels(G, pos, font_size=6)
    nx.draw_networkx_edge_labels(G, pos, list, font_size=5, label_pos=0.5)
    plt.savefig("./templates/" + input + "关系图.png", dpi=350)
    Dir.append("./templates/" + input + "关系图.png")

    fig=plt.figure(input + "高管关系图")
    pos = nx.spring_layout(H)
    nx.draw_networkx_nodes(H, pos, node_color='pink')
    nx.draw_networkx_edges(H, pos, edge_color='red')
    nx.draw_networkx_labels(H, pos, font_size=6)
    nx.draw_networkx_edge_labels(H, pos, list2, font_size=3, label_pos=0.5)
    plt.title(input + "高管关系图")

    plt.savefig("./templates/" + input + "高管关系图.png", dpi=350)
    Dir.append("./templates/" + input + "高管关系图.png")
    # plt.show()
    return 1,Dir

def search_company_shortname(input):
    res=SPO.find({"prop":"证券简称","obj":input})
    if res==None:
        return 0,None,None
    res=list(res)
    ans,Dir=search_company_fullname(res[0]['sub'])
    return ans,res[0]['sub'],Dir
def search_manager(input):
    # res=SPO.find({'obj':input,'prop':"高管"})
    res2 = Person.find({'姓名': input})
    res2 = list(res2)
    if len(res2) == 0:
        return 0,None
    ans=[]

    for i in res2:
        code=i["代码"]
        company=Company.find({"代码":code})
        company=list(company)
        #一个代码最多对应一个公司，否则就没有
        if len(company)==0:
            pass
        else:
            company_name = company[0]["公司名称"]

            fig=plt.figure(company_name+input+"背景图")
            G=nx.Graph()
            G.add_node(input)
            G.add_node(company_name)
            G.add_edge(input,company_name,weight=0.5)
            list1={}
            list1.update({(input,company_name):i["职务"]})
            for key in i:
                if key=="代码" or key=="职务" or key=="_id" or key=="姓名":
                    pass
                else:
                    G.add_node(i[key])
                    G.add_edge(input,i[key],weight=0.5)
                    list1.update({(input,i[key]):key})
            pos = nx.spring_layout(G)
            nx.draw_networkx_nodes(G, pos, node_color='pink')
            nx.draw_networkx_edges(G, pos, edge_color='red')
            nx.draw_networkx_labels(G, pos, font_size=6)
            nx.draw_networkx_edge_labels(G, pos, list1, font_size=5, label_pos=0.5)
            plt.title(company_name+input+"背景图")
            plt.savefig("./templates/" + company_name+input + "背景图.png", dpi=350)
            ans.append("./templates/" + company_name+input + "背景图.png")
    return 1,ans
#只能输入 简称 全程 姓名
def search(input):
    id,fullname,Dir=search_company_shortname(input)
    if id==1:
        for i in Dir:
            print(i)






if __name__=="__main__":
    # search_company_shortname("万  科Ａ")
    # a,comp=search_manager("王石")
    search("万  科Ａ")




































