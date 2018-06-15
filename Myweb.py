from flask import Flask
from flask import render_template
from flask import request
from model import search,pyhtml
from flask import redirect,url_for

app = Flask(__name__)
class search_unit:
    def __init__(self,search_input_text,img_path):
        self.search_text=search_input_text
        self.img_list=img_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=="POST":
        global search_input
        global path
        search_input=request.form["search_input"]
        # print(search_input)
        id,word,path=search(search_input)
        if id==0:
            return redirect(url_for("error"))
        if id==1:
            hh=search_unit(search_input,path)
            return redirect(url_for("results"))
    return render_template("index.html")

@app.route('/error/')
def error():
    return render_template("fornone.html")
@app.route('/results/',methods=['GET', 'POST'])
def results():
    global search_input
    global path
    if request.method=="POST":
        return redirect(url_for('index'))
        # print("哈哈哈啊")

    #md 老子自己写一个生产html文件的库
    m=pyhtml(search_input)
    for i in path:
        m.add_img(i.strip('\ufeff'))
    href=m.close()
    return render_template(href)






if __name__ == '__main__':

    app.run()
