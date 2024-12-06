from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('job/<str:pk>/', views.job, name="job"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-job/', views.createJob, name="create-job"),
    path('update-job/<str:pk>/', views.updateJob, name="update-job"),
    path('delete-job/<str:pk>/', views.deleteJob, name="delete-job"),
]