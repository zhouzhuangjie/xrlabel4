"""xrlabel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import views as static_views
from xray import views

urlpatterns = [
  url(r'^diagnose$', views.diagnose),
  url(r'^main$', views.main),

  url(r'^$', views.main),
  url(r'^login$', views.login),
  url(r'^logout$', views.logout),
  url(r'^task$', views.task),
  url(r'^upload$', views.upload),
  url(r'^download$', views.download),
  url(r'^reset$', views.reset),
  url(r'^count_dr$', views.count_dr),

  # url(r'^xrstatic/images/(?P<image_path>.*)$',views.imageview)

]
