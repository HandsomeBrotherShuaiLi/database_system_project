from flask import Flask
from flask import render_template
from flask import request
from model import search,pyhtml
from flask import redirect,url_for
from model import User,db,Company,SPO,Person
import datetime
from flask_admin import Admin
from flask_admin.contrib.pymongo import ModelView, filters
from flask_admin.contrib.pymongo.filters import BooleanEqualFilter
from wtforms import form, fields
from flask_admin.model.fields import InlineFormField, InlineFieldList
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456790'
class search_unit:
    def __init__(self,search_input_text,img_path):
        self.search_text=search_input_text
        self.img_list=img_path
class loginError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
@app.route('/search/', methods=['GET', 'POST'])
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
#user={'name':   'password':   lasttime:    count:     isadmin: search:}
@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method=="POST":

        name=request.form["username"]
        password=request.form["password"]
        if name is None or password is None:
            return render_template("login.html")
        else:
            res=User.find({'name':name,'password':password})
            user=list(res)
            #用户名密码错误
            if len(user)==0:

                return render_template("login.html")
            else:
                if user[-1]['isadmin']==1:
                    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    count = user[-1]['count'] + 1
                    User.update({"name": name, "password": password}, {"$set": {"lasttime": nowTime, "count": count}})

                    return redirect(url_for("admin.index"))
                else:
                    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    count=user[-1]['count']+1
                    User.update({"name":name,"password":password},{"$set":{"lasttime":nowTime,"count":count}})
                    return redirect(url_for("index"))
    return render_template("login.html")


@app.route('/Register/', methods=['GET', 'POST'])
def reg():
    if request.method=="POST":
        name = request.form["username"]
        password = request.form["password"]
        if name is None or password is None:
            return render_template("register.html")
        else:
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            count = 1
            search_list=list()
            User.insert({"name":name,"password":password,"lasttime":nowTime,"count":count,"isadmin":0})
            return redirect(url_for("index"))

    return render_template("register.html")


class InnerForm(form.Form):
    name = fields.StringField('Name')
    test = fields.StringField('Test')


class UserForm(form.Form):
    name = fields.StringField('Name')

    password = fields.StringField('Password')

    count = fields.StringField('Count')
    lasttime = fields.StringField('Lasttime')

    isadmin = fields.StringField('is admin ?')
    # Form list
    form_list = InlineFieldList(InlineFormField(InnerForm))

class UserView(ModelView):
    column_list = ('name',  'password','count','lasttime','isadmin',)
    column_sortable_list = ('name',  'password','count','lasttime','isadmin',)

    form = UserForm

class CompanyForm(form.Form):
    adress = fields.StringField('公司注册地址')

    stockname = fields.StringField('证券简称')

    company_name= fields.StringField('公司名称')
    manager = fields.StringField('总经理')

    id = fields.StringField('注册号')
    place= fields.StringField('首次注册登记地点')
    faren = fields.StringField('法人代表')
    email=fields.StringField("公司注册地址邮箱")
    code=fields.StringField("代码")
    # Form list
    form_list = InlineFieldList(InlineFormField(InnerForm))

class CompanyView(ModelView):
    column_list = ('公司注册地址',  '证券简称','公司名称','总经理','注册号','首次注册登记地点','法人代表',"公司注册地址邮箱","代码")
    column_sortable_list = ('公司注册地址',  '证券简称','公司名称','总经理','注册号','首次注册登记地点','法人代表',"公司注册地址邮箱","代码")

    form = CompanyForm


class PersonForm(form.Form):
    do_what = fields.StringField('职务')

    managername = fields.StringField('姓名')

    birthday= fields.StringField('出生年月')
    sex= fields.StringField('性别')
    code=fields.StringField("代码")
    edu = fields.StringField("学历")

    # Form list
    form_list = InlineFieldList(InlineFormField(InnerForm))

class PersonView(ModelView):
    column_list = ('职务',  '姓名','出生年月','性别',"代码","学历")
    column_sortable_list = ('职务',  '姓名','出生年月','性别',"代码","学历")

    form = PersonForm


class SPOForm(form.Form):
    obj= fields.StringField('obj')

    prop = fields.StringField('prop')

    sub= fields.StringField('sub')
    time= fields.StringField('updata_time')
    type=fields.StringField("type")


    # Form list
    form_list = InlineFieldList(InlineFormField(InnerForm))

class SPOView(ModelView):
    column_list = ('obj',  'prop','sub','updata_time',"type")
    column_sortable_list = ('obj',  'prop','sub','updata_time',"type")
    form = SPOForm
if __name__ == '__main__':

    admin=Admin(app,name="知识图谱后台管理", template_mode='bootstrap3')
    admin.add_view(UserView(db.User, '用户管理'))
    admin.add_view(CompanyView(db.Company,"证券管理"))
    admin.add_view(PersonView(db.Person,"高管管理"))
    admin.add_view(SPOView(db.SPO,"SPO管理"))


    app.run(debug=True)

