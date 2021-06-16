from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from datetime import date

from app.models import Profile, Question, Tag, Answer
from app.models import VoteForAnswer, VoteForQuestion

def paginate(content_list, request, num_per_page):
    paginator = Paginator(content_list, num_per_page)

    page = request.GET.get("page")
    content_list = paginator.get_page(page)
    return content_list

def index(request):
    questions = Question.objects.new_questions()
    content = paginate(questions, request, 5)
    return render(request, 'index.html', {'content': content})

def ask(request):
    return render(request, 'ask.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def hot(request):
    questions = Question.objects.hot_questions()
    content = paginate(questions, request, 5)
    return render(request, 'index.html', {'content': content})

def tag(request, tag_name):
    questions = Question.objects.tag_questions(tag_name)
    content = paginate(questions, request, 5)
    return render(request, 'tag.html', {'content': content, 'tag_name': tag_name})


def question(request, pk):
    selected_question = Question.objects.single_question(pk)
    selected_answers = Answer.objects.filter(question=selected_question)
    content = paginate(selected_answers, request, 3)
    return render(request, 'question.html', {'question': selected_question, 'content': content})
