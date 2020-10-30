from django.shortcuts import render, redirect, HttpResponsePermanentRedirect
from .models import College, Exam, Question, Option, Record
from django.core.paginator import Paginator
from .forms import CreateUserForm, StudentForm, UserAuthentication, ExamForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from django.contrib import messages
from django.urls import reverse
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
                return redirect(reverse('exam:signin'))
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
        else:
            messages.warning(request, "Invalid Credentials")

    context= {'auth_form':auth_form}
    return render(request, template_name='exam/signin.html', context = context)


@login_required
@allowed_users(allowed_roles=['student'])
def signout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='exam:signin')
@allowed_users(allowed_roles=['student'])
def selectExam(request):
    exams = Exam.objects.filter(college = request.user.student.college.id)
    if request.method == "POST":
        exam = request.POST['exam']
        exam = Exam.objects.filter(exam_name=exam, college=request.user.student.college.id)
        return redirect(reverse('exam:home',kwargs={'exam_id' : exam[0].id}))
    context = {'exams':exams}
    return render(request, 'exam/select_college.html', context)


@login_required(login_url='exam:signin')
@allowed_users(allowed_roles=['student'])
def home(request, exam_id):
    question = Question.objects.filter(exam=exam_id)
    global answer_list
    answer_list = []
    global question_list
    question_list = list(question)
    for question in question_list:
        Record.objects.create(student_id=request.user.id, exam_id=exam_id, question_id=question.id)
    random.shuffle(question_list)
    return render(request, 'exam/home.html', {'exam_id':exam_id})

@login_required(login_url='exam:signin')
@allowed_users(allowed_roles=['student'])
def exam(request, id):
    global question_list
    exam_question = question_list[:]
    option_list = []
    for ques in exam_question:
        option = Option.objects.get(question=ques.id)
        option_list.append(option)

    context = {'questions': exam_question, 'questions_page': exam_question, 'option_list': option_list, 'exam_id':id}
    return render(request, 'exam/exam.html', context)

@login_required
def saveans(request):
    question_id = request.GET['qid']
    answer = request.GET['ans']
    exam_id = request.GET['eid']
    Record.objects.filter(question_id=question_id, exam_id=exam_id, student_id=request.user.id).update(answer=answer)
    

@login_required(login_url='exam:signin')
@allowed_users(allowed_roles=['student'])
def result(request):
    score = 0
    global question_list
    compare_list = question_list[:]
    for question in compare_list:
        record = Record.objects.get(question_id=question.id)

        if record.answer == question.answer:
            score += 2
    return render(request, 'exam/result.html', {'score':score})
