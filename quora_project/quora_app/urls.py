from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginpg, name="login"),
    path('signUp/', views.signup, name="signup"),
    path('logout/', views.logoutView, name="logout"),
    path('home/<str:user>', views.questions, name="main"),
    path('dashboard/', views.post_questions, name="dashboard"),
    path('answer_submit/<str:answer>/<str:ques_id>', views.submit_answer, name="submit_answer"),
]
