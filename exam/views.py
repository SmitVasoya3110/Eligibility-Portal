from django.shortcuts import render, redirect
from .models import College, Exam, Question, Option
from django.core.paginator import Paginator
from .forms import CreateUserForm, StudentForm, UserAuthentication, ExamForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from django.contrib import messages

import random


# Create your views here.
global question_list
global answer_list


def register(request):
    user_form = CreateUserForm()
    student_form = StudentForm()
    if request.method == "POST":
        user_form = CreateUserForm(request.POST)
        student_form = StudentForm(request.POST)
     
        if user_form.is_valid() and student_form.is_valid():
            try:
                username = user_form.cleaned_data['username']
                college = student_form.cleaned_data["college"]
                roll_no = student_form.cleaned_data.get("roll_no")
                user = user_form.save(commit=False)
                user.college = college
                user.roll_no = roll_no
                user.save()
                messages.success(request, f"{username} created successfully")
                return redirect('signin')
            except Exception as e:
                messages.warning(request, "Please Enter Valid/Unique(username, email)/Strong Data")

           
        else:
            messages.warning(request, "Please Enter Valid/Unique(username, email)/Strong Data")

    context ={'user_form':user_form,'student_form':student_form}
    return render(request, 'exam/register.html', context)

def signin(request):
    auth_form = UserAuthentication()
    if request.method == "POST":
        user = authenticate(request, username = request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('/')

    context= {'auth_form':auth_form}
    return render(request, 'exam/signin.html', context)


@login_required
@allowed_users(allowed_roles=['student'])
def signout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='signin')
@allowed_users(allowed_roles=['student'])
def selectExam(request):
    exams = Exam.objects.filter(college = request.user.student.college.id)
    if request.method == "POST":
        exam = request.POST['exam']
        exam = Exam.objects.filter(exam_name=exam, college=request.user.student.college.id)
        return redirect(home, exam_id=exam[0].id)
    context = {'exams':exams}
    return render(request, 'exam/select_college.html', context)


@login_required(login_url='signin')
@allowed_users(allowed_roles=['student'])
def home(request, exam_id):
    question = Question.objects.filter(exam=exam_id)
    global answer_list
    answer_list = []
    global question_list
    question_list = list(question)
    random.shuffle(question_list)
    return render(request, 'exam/home.html', {'exam_id':exam_id})

@login_required(login_url='signin')
@allowed_users(allowed_roles=['student'])
def exam(request):
    global question_list
    exam_question = question_list[:]
    option_list = []
    for ques in exam_question:
        option = Option.objects.get(question=ques.id)
        option_list.append(option)

    context = {'questions': exam_question, 'questions_page': exam_question, 'option_list': option_list}
    return render(request, 'exam/exam.html', context)

@login_required(login_url='signin/')
@allowed_users(allowed_roles=['student'])
def result(request):
    if request.method == "POST":
        user_ans = request.POST
        id_lst = []
        answers = []
        score = 0
        for ans, value in user_ans.items():
            if ans == 'csrfmiddlewaretoken':
                continue
            id_lst.append(ans[3:])
            answers.append(value)
        for i in range(len(id_lst)):
            ans = Question.objects.get(id=id_lst[i])
            ans = ans.answer
            if ans == answers[i]:
                score += 2
        
        return render(request, 'exam/result.html',{'score':score})
    return render(request, 'exam/result.html')

@login_required
def saveans(request):
    global answer_list
    print(request)