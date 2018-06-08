from django.shortcuts import HttpResponse
import App.models as models
from django.shortcuts import render_to_response
from django.views.decorators import csrf
import datetime
def form(request):
    return render_to_response('post.html')
def login(request):
    ctx={}
    if request.GET:
        name=request.GET['name']
        psw=request.GET['psw']
        list=models.User.objects.all()
        for var in list:
            if name==var.name and psw==var.psw:
                var.count+=1
                timelast=var.timenow
                var.timenow=datetime.datetime.now()
                var.save()
                res="用户"+name+'第'+str(var.count)+'次登录,上次登录时间是'+str(timelast)

                return HttpResponse('<p>'+res+'</p>')
        models.User.objects.create(name='name',psw=psw,timenow=datetime.datetime.now(),count=1)
        res = "用户" + name + '第1次登录'
        return HttpResponse('<p>' + res + '</p>')




