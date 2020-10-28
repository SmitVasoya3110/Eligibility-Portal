from django.urls import path
from . import views

app_name = 'adminapp'
urlpatterns = [
    path('', views.home, name="adminhome"),
    path('loginadmin/', views.loginAdmin, name="loginadmin"),
    path('logoutadmin/', views.logoutAdmin, name="logoutadmin"),

    path('college-student/<int:id>', views.fetchStudents, name="college-student"),
    path('all-students-data/', views.allStudents, name="all-students-data"),
    path('college-exam/<int:id>', views.fetchExams, name="college-exam"),
    path('exam/', views.exam, name="exam"),
    path('exam-info/<int:id>', views.examInfo, name="exam-info"),


    path('adminuser/', views.fetchAdmin, name="adminuser"),
    path('addcollege/', views.addCollege, name="addcollege"),
    path('addexam/', views.addExam, name="addexam"),
    path('addadmin/', views.addAdmin, name="addadmin"),
    path('addquestion/<int:id>', views.addQuestion, name="addquestion"),
    path('addoption/<int:id>', views.addOption, name="addoption"),
    path('edit-question/<int:exam_id>/<int:q_id>', views.editQuestion, name="edit-question"),
]
