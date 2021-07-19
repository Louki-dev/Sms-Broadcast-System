"""Base URL Configuration

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
from django.urls import path, include
from Sms.views import Contact_view, index, Contact_add, Globelabs_api, Opt_in_users, \
    Create_message, junction, adminView, how_to_opt_in, search, about_request
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('user/', include('User_login.urls')),
    path('user/admin/dashboard/', adminView, name="admin"),
    path('user/admin/contacts/', Contact_view, name="contacts"),
    path('user/admin/opt-in/list/', Opt_in_users, name="opt_in_users"),
    path('user/admin/message/', Create_message.as_view(), name='create_message'),
    path('user/admin/search/', search, name="search"),
    path('new/contact-form/', Contact_add, name="contact_form"),
    path('new/opt-in/', how_to_opt_in, name="opt_in"),
    url(r'^api/globelabs/', Globelabs_api), # web hook for opt-in parameters
    path('api/sent/', junction, name='junction'),
    path('about/', about_request, name='about'),

]
