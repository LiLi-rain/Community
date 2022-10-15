from django.urls import include,path

from .views import CreatQuestionView, QuestionDetailView, QuestionListView
from .views import create_answer


app_name = 'questions'  #路由命名空间

urlpatterns = [
    path('questions/',include(([
        path('', QuestionListView.as_view(), name='questions_list'),
        path('add/', CreatQuestionView.as_view(), name='create_question'),
        path('<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
        path('<int:pk>/add', create_answer, name='create_answer'),
    ])))
]