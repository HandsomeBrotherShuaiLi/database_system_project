import pymongo
from pyecharts import Graph
client=pymongo.MongoClient()
db=client.Mydatabase
Company=db.Company
Person=db.Person
SPO=db.SPO
#通过公司来查
#pyecharts 做graph的时候，对于节点数量以及name的字数限制比较严格，故考虑改成networkx
# def search(input):
#    res=list(SPO.find({"sub":input}))
#    print(len(res))
#
#    nodes=[]
#
#    node={}
#    node["name"] = input
#    node["symbolSize"] = 20
#
#    nodes.append(node)
#
#    links=[]
#    # nodes.append({'name': res[0]['obj'], 'symbolSize': 10})
#    # nodes.append({'name': res[1]['obj'], 'symbolSize': 10})
#    # nodes.append({'name': res[2]['obj'], 'symbolSize': 10})
#    # nodes.append({'name': res[3]['obj'], 'symbolSize': 10})
#    # nodes.append({'name': res[4]['obj'], 'symbolSize': 10})
#    # nodes.append({'name': res[5]['obj'], 'symbolSize': 10})
#    # nodes.append({'name': res[6]['obj'], 'symbolSize': 10})
#    # # nodes.append({'name': res[7]['obj'], 'symbolSize': 10})
#    # # nodes.append({'name': res[8]['obj'], 'symbolSize': 10})
#    for i in range(5):
#        nodes.append({'name': str(res[i]['obj'][0]), 'symbolSize': 10})
#
#
#    for i in nodes:
#        for j in nodes:
#            links.append({"source": i.get('name'), "target": j.get('name'),'value':50})
#    m = Graph(title=(input + "关系图"), height=600, width=1200)
#
#
#    m.add("",nodes,links,line_color="#aaa")
#    m.show_config()
#    m.render()


if __name__=="__main__":
    # search("平安银行股份有限公司")









