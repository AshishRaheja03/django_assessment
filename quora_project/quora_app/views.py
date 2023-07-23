from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .models import Question, Answer
from django.forms import ModelForm
from .forms import UserForm
from django.contrib.auth import authenticate, logout, login

# Create your views here.
def loginpg(request):
    if(request.user.is_authenticated):
        return redirect(f'/home/{request.user}', user=request.user)
    
    if(request.method == 'POST'):
        login_form=AuthenticationForm(data=request.POST)
        if(login_form.is_valid()):
            print("this is REQUEST", request.POST['username'])
            usernm=request.POST['username']
            passw=request.POST['password']
            user = authenticate(request, username=usernm, password=passw)
            login(request, user)
            print("USER_LOGIN")
            return redirect(f'/home/{user}', user=user)
        else:
            login_form=AuthenticationForm()
            context={
            'login_form':login_form,
            'error_msg': "Wrong Username or Password"
        }

    else:
        login_form=AuthenticationForm()
        context={
            'login_form':login_form,
        }
    return render(request, 'templates/login.html', context=context)

def logoutView(request):
    logout(request)
    return redirect('login')

def signup(request):
    userForm = UserForm()
    if(request.user.is_authenticated):
        return redirect('main')

    if(request.method == 'POST'):
        userForm = UserForm(request.POST)
        print(userForm.is_valid(),request.POST)
        
        if(userForm.is_valid()):
            user=userForm.save() 
            user.save()

            user = authenticate(request, username=userForm.cleaned_data['username'], password=userForm.cleaned_data['password1'])
            login(request, user)
            print("USER SIGNUP AUTHENTICATED")

            return redirect('/')
    
    context={
        'userForm':userForm,
    }
            
    return render(request, 'templates/signUp.html', context)

def questions(request, user):
    if(not request.user.is_authenticated):
        return redirect('login')
    question_answers={}

    if(len(Question.objects.all())>0):
        all_questions=Question.objects.exclude(user=request.user)
    else:
        all_questions=''

    success_msg=""
    for ques in all_questions:
        answers=Answer.objects.filter(question=ques)
        question_answers[(ques.id, ques.question_text)]=[a.answer_text for a in answers]
    if(request.method == 'POST'):
        answer=Answer()
        user_answer=request.POST['answer']
        if(user_answer == "" or user_answer is None):
            return render(request, 'templates/questions.html', 
                  context={'user':user,
                           'question_answers': question_answers,
                           'success_msg':success_msg})
        ques_id=request.POST['ques_id']        
        answer.user=request.user
        answer.answer_text=user_answer
        ques=Question.objects.get(id=ques_id)
        answer.question=ques
        answer.save()
        
        success_msg="your answer saved succesfully. refresh to load"

    return render(request, 'templates/questions.html', 
                  context={'user':user,
                           'question_answers': question_answers,
                           'success_msg':success_msg})

def submit_answer(request, answer, ques_id):
    answer=Answer()
    answer.user=request.user
    answer.answer_text=answer
    ques=Question.objects.get(id=ques_id)
    answer.question=ques
    answer.save()

def post_questions(request):
    if(request.user.is_authenticated):
        all_ques=Question.objects.all().filter(user=request.user)

        if(request.method == 'POST'):
            ques=Question()
            ques.question_text=request.POST['question_text']
            ques.user=request.user
            ques.save()


        context={
            'all_ques':all_ques,
        }
        return render(request, 'templates/dashboard.html', context)
    else:
        return redirect('/')