"""askmeLenkova URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ask/', views.ask, name='ask'),
    path('hot/', views.hot, name='hot'),
    path('login/', views.login, name='login'),
<<<<<<< HEAD
    path('question/<int:pk>/', views.question, name='question'),
    path('settings/', views.settings, name='settings'),
    path('signup/', views.signup, name='signup'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('', views.index, name='index')
=======
    path('question/<int:pk>/', views.question, name='one_question'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('tag/<str:tag>/', views.tag, name='tag'),
    path('hot/', views.hot, name='hot'),
    path('', views.index, name='index'),

>>>>>>> a0896c2174ea462ef2b0a72a7e51fccaecfd71b2
]
