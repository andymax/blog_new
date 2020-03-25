"""blog_new URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from article import views
from django.urls import path

app_name='article'
urlpatterns = [

    path('',views.index,name='index'),
    path('posts/<int:pk>/',views.detail,name='detail'),
    path('archives/<int:year>/<int:month>/',views.archive,name='archive'),
    path('categories/<int:pk>/',views.category,name='category'),
    path('tags/<int:pk>/',views.tag,name='tags'),
    path('search/',views.search,name='search'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('register',views.register,name='register'),

]
