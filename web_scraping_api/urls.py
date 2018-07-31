from django.conf.urls import url
from django.contrib import admin
from scraping_app import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/(?P<version>(v1))/articles/$', views.ArticlesList.as_view(), ),
    url(r'^api/(?P<version>(v1))/subjects/$', views.SubjectList.as_view(), ),
]