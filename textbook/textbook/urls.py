"""
URL configuration for textbook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from . import views

urlpatterns = [
    path('hello', views.heythere),
    path('admin/', admin.site.urls),
    path('new',views.form_for_your_own_new_textbook),
    path('new/',views.form_for_your_own_new_textbook),
    path('create', views.handle_form_submission),
    path('create/', views.handle_form_submission),
    path('books', views.show_textbook_list),
    path('books/', views.show_textbook_list),
    path('/', views.homepage),
    path('', views.homepage),
]
