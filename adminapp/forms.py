from exam.models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm



class AddCollegeForm(ModelForm):
    class Meta:
        model = College
        fields = '__all__'


class AddExamForm(ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model =  User
        fields = ['username', 'email','is_superuser','is_staff']

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = "__all__"


class OptionForm(ModelForm):
    class Meta:
        model = Option
        fields = "__all__"
  