from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.mainpage'),
    url(r'^questionnaire/$','main.views.questionnaire'),
    url(r'^register/$','main.views.register'),
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout),
    url(r'^about/$','main.views.mainpage'),
    url(r'^contact/$','main.views.mainpage'),
    url(r'^importperson/$','main.views.importperson'),
    url(r'^adno/(?P<adno>\w+)/$','main.views.personbyadno'),
    url(r'^manage/$','main.views.manage'),
    url(r'^manage/(?P<adno>\w+)/$','main.views.manage'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)


#Todo
'''
mainpage
register
login
logout

'''