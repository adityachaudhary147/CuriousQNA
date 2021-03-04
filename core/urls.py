from .views import RegisterView,LoginView,DashboardView,LogoutView,QuestionView,AnswerView,QuestionSingleView,Like,AboutView
from django.urls import path

urlpatterns=[
    path('register/',RegisterView.as_view(),name='register-view'),
    path('login/', LoginView.as_view(), name='login-view'),
    path('', DashboardView.as_view(), name='dashboard-view'),
    path('logout/', LogoutView.as_view(), name='logout-view'),
    path('question/',QuestionView.as_view(),name='question-view'),
    path('question/<int:pk>',QuestionSingleView.as_view(),name='question-single-view'),
    path('answer/<int:pk>',AnswerView.as_view(),name='answer-view'),
    path('like/',Like.as_view(),name='ans-like'),
    path('about/',AboutView.as_view(),name='about-view'),

]