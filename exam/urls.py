from django.urls import path
from . import views

urlpatterns = [
    path('', views.selectExam, name="select-exam"),
    path('home/<int:exam_id>', views.home, name='home'),
    path('signup/', views.register, name="signup"),
    path('signin/',views.signin, name="signin"),
    path('startexam/', views.exam, name="startexam"),
    path('saveans/', views.saveans, name="saveans"),
    
    path('result/', views.result, name="result"),
    path('logout/', views.signout, name="logout"),
]
