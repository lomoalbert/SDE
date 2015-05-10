#coding=utf8
from django.db import models


class Person(models.Model):
    username= models.CharField(max_length=30) # 用户名
    name = models.CharField(max_length=30) # 姓名
    sex = models.CharField(max_length=30) # 性别
    age = models.CharField(max_length=30) # 年龄
    adno = models.CharField(max_length=30) # 住院号
    home = models.CharField(max_length=30) # 住址
    profession = models.CharField(max_length=64)  # 职业
    education = models.CharField(max_length=64)  # 文化程度
    disease_history = models.CharField(max_length=64)  # 既往病史
    disease_age_h = models.CharField(max_length=64)  # 既往病史病龄
    disease_current = models.CharField(max_length=64)  # 现病史
    disease_age_c = models.CharField(max_length=64)  # 现病史病龄
    used_drugs = models.CharField(max_length=64)  # 既往用药
    using_drugs = models.CharField(max_length=64)  # 现用药物

    # addate = models.DateField()
    #bedno = models.IntegerField()


    def __unicode__(self):
        return self.username


class Question(models.Model):
    person = models.ForeignKey(Person)
    q1 = models.IntegerField()
    q2 = models.IntegerField()
    q3 = models.IntegerField()
    q4 = models.IntegerField()
    q5 = models.IntegerField()
    q6 = models.IntegerField()
    q7 = models.IntegerField()
    q8 = models.IntegerField()
    q9 = models.IntegerField()
    a = models.IntegerField()
    b = models.IntegerField()
    c = models.IntegerField()
    d = models.IntegerField()
    e = models.IntegerField()
    f = models.IntegerField()
    g = models.IntegerField()
    h = models.IntegerField()
    i = models.IntegerField()
    j = models.IntegerField()
    score = models.IntegerField()
    time_submit = models.DateTimeField()

    def __unicode__(self):
        return self.person.username