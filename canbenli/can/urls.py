from django.urls import path
from . import views
urlpatterns=[
   
    path('',views.home, name='home'),
    path('articles',views.blog, name='articles'),
    path('contact',views.contact, name='contact'),
    path('projects',views.portfolio, name='projects'),
    path('article-single',views.blog_single, name='article-single'),
    path('articles/<slug:slug>/',views.blog_single,name='blog_single'),
]