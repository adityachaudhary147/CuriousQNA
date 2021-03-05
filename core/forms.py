from django import forms
from .models import User


from questans.models import Question1,Answers,QuestionGroups

class Question1Form(forms.ModelForm):
    class Meta:
        model=Question1
        fields=['title']

class AnswersForm(forms.ModelForm):
    class Meta:
        model=Answers
        fields=['answer_text']

class QuestionGroupsForm(forms.ModelForm):
    class Meta:
        model=QuestionGroups
        fields='__all__'

class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model=User
        fields=['email','first_name','last_name','password','username']


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=['email','password',]
