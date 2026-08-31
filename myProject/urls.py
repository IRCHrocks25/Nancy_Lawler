from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('', views.home, name='home'),
    path('orientation/', RedirectView.as_view(pattern_name='home', permanent=False), name='orientation'),
    path('survey/', RedirectView.as_view(pattern_name='home', permanent=False), name='survey'),
    path('thank-you/', RedirectView.as_view(pattern_name='home', permanent=False), name='thank_you'),
    path('email-copy/', RedirectView.as_view(pattern_name='home', permanent=False), name='email_copy'),
]
