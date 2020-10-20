from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from exam.models import College, Student, Exam, Question, Option
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import AddCollegeForm, AddExamForm, CreateUserForm, QuestionForm, OptionForm
from django.contrib.auth import authenticate, login, logout
from exam.decorators import allowed_users, admin_only
from django.urls import reverse


# Create your views here.

def loginAdmin(request):
    auth_form = AuthenticationForm()
    if request.method == "POST":
        user = authenticate(request, username = request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect(reverse('adminhome'))

    context= {'auth_form':auth_form}
    return render(request, 'adminapp/admin_login.html', context)

@login_required(login_url='loginadmin/')
@allowed_users(allowed_roles=['admin'])
def logoutAdmin(request):
    logout(request)
    return redirect(reverse('adminhome'))

@login_required(login_url='loginadmin/')
@allowed_users(allowed_roles=['admin'])
def home(request):
    college_list = College.objects.all()
    college_count = college_list.count()
    student_count = Student.objects.all().count()
    exam_count = Exam.objects.all().count()

    context = {
        'college_list' : college_list,
        'college_count' : college_count,
        'student_count' : student_count,
        'exam_count' : exam_count
    }
    return render(request, 'adminapp/dashboard.html', context)

@login_required(login_url='loginadmin/')
@allowed_users(allowed_roles=['admin'])
def fetchStudents(request, id):
    students = Student.objects.filter(college=id).prefetch_related('college')
    print(students)
    context = {'students':students}
    return render(request, 'adminapp/studentlist.html', context)

@login_required(login_url='loginadmin/')
@allowed_users(allowed_roles=['admin'])
def allStudents(request):
    all_students = Student.objects.all()

    context = {'all_students':all_students}
    return render(request, 'adminapp/all_students.html', context)  

@login_required(login_url='loginadmin/')
@allowed_users(allowed_roles=['admin'])
def exam(request):
    college_list = College.objects.all()

    context = {'college_list':college_list}
    return render(request, 'adminapp/exam.html', context)

@login_required(login_url='loginadmin/')
@allowed_users(allowed_roles=['admin'])
def fetchExams(request, id):
    exam_list = Exam.objects.filter(college=id).prefetch_related('college')
    context = {'exam_list':exam_list}
    return render(request, 'adminapp/college_exam.html', context)

@login_required(login_url='loginadmin/')
@allowed_users(allowed_roles=['admin'])
def fetchAdmin(request):
    admin_users = User.objects.filter(is_staff=True)
    print(admin_users)

    context = {'admin_users':admin_users}
    return render(request, 'adminapp/all_admin.html', context)

@login_required(login_url='loginadmin/')
@allowed_users(allowed_roles=['admin'])
def addCollege(request):
    college_form = AddCollegeForm()
    if request.method == "POST":
        college_form = AddCollegeForm(request.POST)
        if college_form.is_valid():
            college_form.save()
        return redirect(home)
    context = {'form' : college_form}
    return render(request, 'adminapp/add_college.html', context)

@login_required(login_url='loginadmin/')
@allowed_users(allowed_roles=['admin'])
def addExam(request):
    exam_form = AddExamForm()
    if request.method == "POST":
        exam_form = AddExamForm(request.POST)
        if exam_form.is_valid():
            exam_form.save()
            return redirect(exam)
    context = {'exam_form' : exam_form}
    return render(request, 'adminapp/add_exam.html', context)

@login_required(login_url='loginadmin/')
@allowed_users(allowed_roles=['admin'])
def addAdmin(request):
    admin_form = CreateUserForm(initial={'is_staff':True, "is_superuser":True})
    if request.method == "POST":
        admin_form = CreateUserForm(request.POST)
        if admin_form.is_valid():
            print(True)
            admin_form.save()
            print('ok')
        return redirect(fetchAdmin)
    context = {'admin_form':admin_form}
    return render(request, 'adminapp/create_admin.html', context)

@login_required(login_url='loginadmin/')
@allowed_users(allowed_roles=['admin'])
def examInfo(request, id):
    question_list = Question.objects.filter(exam=id).prefetch_related('exam')
    option_list = []
    for ques in question_list:
        options = Option.objects.filter(question = ques.id)
        if len(options) > 1:
            for option in options:
                if option.question.id == ques.id:
                    option_list.append(option)
        else:
            option = options[0]
            option_list.append(option)
    context = {'question_list':question_list, 'option_list':option_list, 'exam_id':id}
    return render(request, 'adminapp/exam_info.html', context)

@login_required(login_url='loginadmin/')
@allowed_users(allowed_roles=['admin'])
def addQuestion(request, id):
    exam = Exam.objects.get(id=id)
    question_form = QuestionForm(initial={'exam':exam})
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.cleaned_data['question_text']
            question_form.save()
            question = Question.objects.filter(question_text=question).reverse()[0]
            option_form = OptionForm(initial={'question' : question})
            print(option_form)
            context = {'option_form':option_form, 'exam_id':id}
        return render(request, 'adminapp/add_option.html', context)

    context = {'question_form':question_form}
    return render(request, 'adminapp/add_question.html', context)

@login_required(login_url='loginadmin/')
@allowed_users(allowed_roles=['admin'])
def addOption(request, id):
    if request.method == 'POST':
        option_form = OptionForm(request.POST)
        if option_form.is_valid():
            option_form.save()
        return redirect('exam-info',id=id)
    else:
        return HttpResponse("It only can be seen after adding new questions")

@login_required(login_url='loginadmin/')
@allowed_users(allowed_roles=['admin'])
def editQuestion(request, exam_id, q_id):
    question = Question.objects.get(id=q_id)
    option = Option.objects.get(question=q_id)
    
    question_form = QuestionForm(instance=question)
    option_form = OptionForm(instance=option)

    if request.method == "POST":
        question_form = QuestionForm(request.POST, instance=question) 
        option_form = OptionForm(request.POST, instance=option)
        if question_form.is_valid() and option_form.is_valid():
            question_form.save()
            option_form.save()
        return redirect('exam-info', id=exam_id)
    context = {'question_form':question_form, 'option_form':option_form}
    return render(request, 'adminapp/update_question.html', context)