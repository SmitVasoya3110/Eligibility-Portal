from .models import Student
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Exam



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class StudentForm(ModelForm):

    class Meta:
        model = Student
        fields ='__all__'
        exclude = ['user']

class UserAuthentication(AuthenticationForm):
    class Meta:
        model = User
        fields = '__all__'

class ExamForm(ModelForm):
    class Meta:
        model : Exam
        fields : '__all__'
        exclude : 'college'