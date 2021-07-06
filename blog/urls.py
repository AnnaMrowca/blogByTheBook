from django.urls import path
from . import views

""" Creating urls.py in app blog is the best way to assure this application can be used in other projects """

app_name = 'blog' #app_name helps define name are of application, this allows organizing URLs along with application
                # and use name of application while invoking these urls.

urlpatterns = [
    #views of post
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail')
]

