#coding=utf8

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render_to_response
from django.http import HttpResponse
import datetime
from models import Person,Question
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
import json

# Create your views here.
def mainpage(request):
    return render_to_response('mainpage.html',locals())


def register(request):
    if request.method == 'POST' and request.POST.get('password1','1')==request.POST.get('password2','2'):
        print request.POST
        user=User.objects.create_user(username=request.POST.get('username'),
                                      email=request.POST.get('email'),
                                      password=request.POST.get('password1'),
                                    )
        user.is_staff=True
        user.save()
        user=auth.authenticate(username=request.POST.get('username'),password=request.POST.get('password1'))
        auth.login(request,user)
        return HttpResponseRedirect('/')
    return render_to_response("registration/register.html", locals())

@login_required
def questionnaire(request):
    u'''
    get方法:查询用户信息,填充表单中个人信息
    post:查询用户,更新用户信息,计算分数,记录问卷和分数和时间
    '''
    personinfo_name=['name','sex','age','adno','profession','education','disease_history','disease_age_h','disease_current',
                'disease_age_c','used_drugs','using_drugs']
    try:
        person=Person.objects.get(username=request.user.username)
    except Person.DoesNotExist:
        person=None
    if request.method=="GET":
        if person:
            personinfo=person
        return render_to_response('questionnaire.html',locals())
    elif request.method=="POST":
        personinfo={'username':request.user.username}
        for name in personinfo_name:
            personinfo[name]=request.POST.get(name,'')

        if not person:
            person=Person(**personinfo)
        else:
            person=Person.objects.get(username=request.user.username)
            for key in personinfo_name:
                exec("person.{key}=request.POST.get('{key}','')".format(key=key))
        person.save()
        newquestion=Question(person=person,
                            q1=int(request.POST.get('q1','0')),
                            q2=int(request.POST.get('q2','0')),
                            q3=int(request.POST.get('q3','0')),
                            q4=int(request.POST.get('q4','0')),
                            q5=int(request.POST.get('q5','0')),
                            q6=int(request.POST.get('q6','0')),
                            q7=int(request.POST.get('q7','0')),
                            q8=int(request.POST.get('q8','0')),
                            q9=int(request.POST.get('q9','0')),
                            a=int(request.POST.get('a','0')),
                            b=int(request.POST.get('b','0')),
                            c=int(request.POST.get('c','0')),
                            d=int(request.POST.get('d','0')),
                            e=int(request.POST.get('e','0')),
                            f=int(request.POST.get('f','0')),
                            g=int(request.POST.get('g','0')),
                            h=int(request.POST.get('h','0')),
                            i=int(request.POST.get('i','0')),
                            j=int(request.POST.get('j','0')),
                            )
        element_A=newquestion.q6
        if newquestion.q2 <=15:
            element_B=newquestion.a
        elif newquestion.q2 <=30:
            element_B=1+newquestion.a
        elif newquestion.q2 <60:
            element_B=2+newquestion.a
        elif newquestion.q2 >60:
            element_B=3+newquestion.a
        if newquestion.q4 > 7:
            element_C=0
        elif newquestion.q4 > 6:
            element_C=1
        elif newquestion.q4 >= 5:
            element_C=2
        elif newquestion.q4 < 5:
            element_C=3
        if newquestion.q3>newquestion.q1:
            Sleep_efficiency=1.0*newquestion.q4/(24-newquestion.q3+newquestion.q1)
        else:
            Sleep_efficiency=1.0*newquestion.q4/(newquestion.q1-newquestion.q3)
        if Sleep_efficiency >0.85:
            element_D=0
        elif Sleep_efficiency >0.75:
            element_D=1
        elif Sleep_efficiency >= 0.65:
            element_D=2
        elif Sleep_efficiency < 0.65:
            element_D=3
        Sleep_disorder=newquestion.b+newquestion.c+newquestion.d+newquestion.e+newquestion.f+newquestion.g+newquestion.h+newquestion.i+newquestion.j
        if Sleep_disorder==0:
            element_E=0
        elif Sleep_disorder <= 9:
            element_E=1
        elif Sleep_disorder <= 18:
            element_E=2
        elif Sleep_disorder <=27:
            element_E=3
        element_F=newquestion.q7
        Daytime_dysfunction=newquestion.q8+newquestion.q9
        if Daytime_dysfunction==0:
            element_G=0
        elif Daytime_dysfunction<=2:
            element_G=1
        elif Daytime_dysfunction<=4:
            element_G=2
        elif Daytime_dysfunction<=6:
            element_G=3
        newquestion.score=element_A+element_B+element_C+element_D+element_E+element_F+element_G
        newquestion.time_submit=datetime.datetime.utcnow()
        newquestion.save()
        well=newquestion.score<=7
        return render_to_response('questionscore.html',locals())


def login(request):
    return render_to_response('login.html',locals())

@login_required
def importperson(request):
    if request.method=="GET":
        return render_to_response('importperson.html',locals())
    fi=request.FILES['personcsv']
    persons=[]
    fi.readline()
    for line in fi.readlines():
        attrs=line.replace('\n','').split(',')
        personlist=Person.objects.filter(adno=attrs[3])
        if personlist:
            person=Person.objects.get(adno=attrs[3])
            person.name=attrs[0]
            person.sex=attrs[1]
            person.age=attrs[2]
            person.dishis=attrs[4]
            person.home=attrs[5]
        else:
            person=Person(name=attrs[0],
                          sex=attrs[1],
                          age=attrs[2],
                          adno=attrs[3],
                          dishis=attrs[4],
                          home=attrs[5]
                          )
        person.save()
        persons.append(person)
    vardict={'persons':persons}
    vardict.update(csrf(request))
    return render_to_response('importperson.html',locals())

def personbyadno(request,adno):
    personlist=Person.objects.filter(adno=adno)
    if not personlist:
        return HttpResponse('None')
    else:
        person=Person.objects.get(adno=adno)
        jsondict={
            'adno':person.adno,
            'name':person.name,
            'sex':person.sex,
            'age':person.age,
            'dishis':person.dishis,
            'home':person.home
        }
        return HttpResponse(json.dumps(jsondict))

@login_required
def manage(request,username=None):
    if not username and not request.user.is_superuser:
        persons=[Person.objects.get(username=request.user.username),]
    elif not username and request.user.is_superuser:
        persons=Person.objects.all()
    elif username and not request.user.is_superuser:
        person=Person.objects.get(username=request.user.username)
        questions=Question.objects.filter(person=person)
    elif username and request.user.is_superuser:
        person=Person.objects.get(username=username)
        questions=Question.objects.filter(person=person)
    return render_to_response('manage.html',locals())