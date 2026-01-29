from django.contrib import admin
from django.urls import path
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('orientation/', views.orientation, name='orientation'),
    path('survey/', views.survey, name='survey'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('email-copy/', views.email_copy, name='email_copy'),
]
