"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from hello_django import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    
    path('ea/', views.EAIndexView.as_view(), name='ea/index'),
    path('ea/<int:pk>/', views.EADetailView.as_view(), name='ea/detail'),
    path('ea/edit/<int:pk>/', views.eaEdit, name='ea/edit'),
    path('ea/create/', views.eaCreate, name='ea/create'),
    path('ea/delete/<int:pk>/', views.eaDelete, name='ea/delete'),

    path('lender/', views.lenderIndexView.as_view(), name='lender/index'),
    path('lender/<int:pk>/', views.lenderDetailView.as_view(), name='lender/detail'),
    path('lender/edit/<int:pk>/', views.lenderEdit, name='lender/edit'),
    path('lender/create/', views.lenderCreate, name='lender/create'),
    path('lender/delete/<int:pk>/', views.lenderDelete, name='lender/delete'),

    path('loan/', views.loanIndexView.as_view(), name='loan/index'),
    path('loan/<int:pk>/', views.loanDetailView.as_view(), name='loan/detail'),
    path('loan/edit/<int:pk>/', views.loanEdit, name='loan/edit'),
    path('loan/create/', views.loanCreate, name='loan/create'),
    path('loan/delete/<int:pk>/', views.loanDelete, name='loan/delete'),
    path('loan/predict/<int:pk>/', views.loanPredict, name='loan/predict'),

]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
