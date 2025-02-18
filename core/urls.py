"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from app.views import DashboardStatsAPIView,SponsorDetailAPIView,StudentSponsorCreateAPIView,StudentListAPIView,DashboadGraphAPIView,StudentSponsorUpdateAPIView,SposorListAPIView,StudentCreate,StudentSponsor,SponsorListCreateAPIView,StudentUpdate
from django.conf.urls.i18n import set_language
# from django.conf.urls.i18n import set_language
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('set_language/', set_language, name='set_language'),
    path('dashboard/',DashboardStatsAPIView.as_view()),
    path('sponser/<int:pk>/',SponsorDetailAPIView.as_view()),
    path('founder/',StudentSponsorCreateAPIView.as_view()),
    path('students/',StudentListAPIView.as_view()),
    path('student_count/',DashboadGraphAPIView.as_view()),
    path('update_founder/<int:pk>/',StudentSponsorUpdateAPIView.as_view()),
    path('sponser_list/',SposorListAPIView.as_view()),
    path('studentcreate/',StudentCreate.as_view()),
    path('student_sponser/<int:pk>/',StudentSponsor.as_view()),
    path('sponser1/',SponsorListCreateAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('studentupdate/<int:pk>/',StudentUpdate.as_view())



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
