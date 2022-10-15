from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.shortcuts import render, redirect


# Create your views here.

@method_decorator([login_required], name='dispatch')
class CreatQuestionView(CreateView):
    """创建问题的视图类
    """

    model = Question
    form_class = QuestionForm
    template_name = 'questions/ask_question.html'

    def form_valid(self, form):
        question = form.save(commit=False)
        question.user = self.request.user
        question.save()
        messages.success(self.request, '问题创建成功')
        return redirect('questions:question_detail', question.pk)


class QuestionListView(ListView):
    """展示问题列表的视图类
    """

    model = Question
    ordering = ('update_date')
    context_object_name = 'questions'
    template_name = 'questions/questions_list.html'
    queryset = Question.objects.all()
    paginate_by = 10


class QuestionDetailView(CreateView):
    """展示问题详情的视图类
    """

    model = Answer
    form_class = AnswerForm
    template_name = 'questions/question_detail.html'

    def get_context_data(self, **kwargs):
        question_id = self.kwargs.get('pk')
        question = Question.objects.get(pk=question_id)
        kwargs['question'] = question
        if Answer.objects.filter(question=question):
            kwargs['answers'] = Answer.objects.filter(question=question)

        context = super().get_context_data(**kwargs)
        return context


@login_required
def create_answer(request, pk):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer()
            answer.user = request.user  # 设定问题提出人
            answer.question = Question.objects.get(pk=pk)
            answer.description = form.cleaned_data.get('description')
            answer.save()
            messages.success(request, '问题创建成功!')
            return redirect('questions:question_detail', answer.question.pk)
    return redirect('questions:question_detail', pk)
