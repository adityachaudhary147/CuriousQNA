from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.
from django.urls import reverse

from django.views.generic.edit import FormView
from .forms import RegisterForm,LoginForm,Question1Form,AnswersForm
from questans.models import Question1,Answers,QuestionGroups
from django.contrib.auth import login,logout
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import json
from .models import User
from django.shortcuts import get_object_or_404

class Home(FormView):
    def get(self,request):
        return render(request,"home.html")

class DashboardView(FormView):
    def get(self,request):
        content={}
        if request.user.is_authenticated:
            user=request.user
            user.backend='django.contrib.core.backends.ModelBackend'
            # ques_obj=Question1.objects.filter(user=user)
            ques_obj=Question1.objects.all()
            content['userdetail']=user
            ans=[]
            dic_for_q_ans={}
            for x in ques_obj:
                ans_obj=Answers.objects.filter(question=x)
                ans.append(ans_obj)
                dict_rnd=dict()
                for we in ans_obj:
                    st_like_by_req_user=we.likes.filter(id=user.id).exists()
                    dict_rnd[we]=st_like_by_req_user
                dic_for_q_ans[x]=dict_rnd
            content['main']=dic_for_q_ans
            content['request']=request
            return render(request,'dashboard.html',content)
        else:
            return redirect(reverse('login-view'))

class QuestionSingleView(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(QuestionSingleView, self).dispatch(request, *args, **kwargs)

    def get(self,request,pk):
        if request.user.is_anonymous:
            redirect(reverse('login-view'))
        qs=Question1.objects.filter(id=pk)
        qn_qs=Answers.objects.filter(question=qs[0])
        content={}
        content['ques']=qs[0]
        content['ans']=qn_qs
        return render(request,'questionsingle.html',content)

class RegisterView(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self,request):
        content={}
        content['form']=RegisterForm
        return render(request,'register.html',content)
    def post(self,request):
        content={}
        form=RegisterForm(request.POST,request.FILES or None)
        if form.is_valid():
            user=form.save(commit=False)
            user.password=make_password(form.cleaned_data['password'])
            user.save()
            login(request,user)
            return redirect(reverse('dashboard-view'))
        content['form']=form
        template='register.html'
        return render(request,template,content)

class LoginView(FormView):

    content = {}
    content['form'] = LoginForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        content = {}
        if request.user.is_authenticated:
            return redirect(reverse('dashboard-view'))
        content['form'] = LoginForm
        return render(request, 'login.html', content)

    def post(self, request):
        content = {}
        email = request.POST['email']
        password = request.POST['password']
        try:
            users = User.objects.filter(email=email)
            user = authenticate(request, username=users.first().username, password=password)
            login(request, user)
            return redirect(reverse('dashboard-view'))
        except Exception as e:
            content = {}
            content['form'] = LoginForm
            content['error'] = 'Unable to login with provided credentials' + e
            return render_to_response('login.html', content)

class QuestionView(FormView):

    content = {}
    content['form'] = Question1Form

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(QuestionView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        content = {}
        if not request.user.is_authenticated:
            return redirect(reverse('login-view'))
        content['form'] = Question1Form
        return render(request, 'question.html', content)

    def post(self, request):
        content = {}
        form=Question1Form(request.POST)
        if form.is_valid():
            ques=form.save(commit=False)
            ques.user=request.user
            ques.save()
        content['form']=Question1Form()
        return render(request,'question.html',content)

class AnswerView(FormView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AnswerView, self).dispatch(request, *args, **kwargs)
    
    def get(self,request,pk):
        content={}
        if not request.user.is_authenticated:
            return redirect(reverse('login-view'))
        content['form']=AnswersForm
        qs=Question1.objects.filter(id=pk)
        part_ques=qs[0]
        content['part_ques']=part_ques
        return render(request,'answer.html',content)
    def post(self,request,pk):
        content={}
        form=AnswersForm(request.POST)
        if form.is_valid():
            ans=form.save(commit=False)
            if ans.is_anonymous==False:
                ans.user=request.user
            else:
                ans.user=User(email=None,username=None,password=None)
            qs=Question1.objects.filter(id=pk)
            part_ques=qs[0]
            content['part_ques']=part_ques
            ans.question=qs[0]
            ans.save()
        content['form']=AnswersForm()
        return render(request,'answer.html',content)

class LogoutView(FormView):
    def get(self, request):
        logout(request)
        return redirect(reverse('login-view'))


class AboutView(FormView):
    def get(self, request):
        return render(request,'About.html')


class Like(FormView):
    def post(self,request):
        user=request.user
        pk=request.POST.get('pk')
        ans=Answers.objects.get(id=pk)
        print("hello1")
        print()
        print(ans.likes.filter(id=request.user.id).exists())
        psta =ans.likes.filter(id=request.user.id).exists()
        if ans.likes.filter(id=request.user.id).exists():
            print("inside if")
            ans.likes.remove(user)
            message='You disliked the answer'
        else:
            ans.likes.add(user.id)
            message='You liked this answer'
        yu=ans.count_likes()
        ctx = {'likes_count': yu , 'message': message}
        print("hello2")
        sta=ans.likes.filter(id=request.user.id).exists()
        
        return JsonResponse({'ctx': yu,"sta":sta,"psta": psta },safe=False)
