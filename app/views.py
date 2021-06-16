from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from app.models import User, Question, Answer
from django.core.exceptions import ObjectDoesNotExist


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)

def index(request):
    questions = Question.objects.new_questions()
    page = paginate(questions, request, 5)
    return render(request, 'index.html', {
        'page_obj': page
    })

def hot(request):
    questions = Question.objects.hot_questions()
    page = paginate(questions, request, 5)
    return render(request, 'index.html', {
        'page_obj': page
    })


def question(request, pk):
    try:
        question = Question.objects.get(id=pk)
        answers = question.answers.best_answers()
        page = paginate(answers, request, 5)
        return render(request, 'question.html', {
            'question': question,
            'page_obj': page
        })
    except ObjectDoesNotExist:
        return render(request, '404_not_found.html')

def tag(request, tag):
    questions = Question.objects.questions_for_tag(tag).all()
    if len(questions) > 0:
        page = paginate(questions, request, 5)
        return render(request, 'tag.html', {
            'page_obj': page,
            'tag': tag
        })
    else:
        return render(request, 'blank_page.html')

def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def settings(request):
    return render(request, 'settings.html')
