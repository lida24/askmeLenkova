<<<<<<< HEAD
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from datetime import date
=======
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from app.models import User, Question, Answer
from django.core.exceptions import ObjectDoesNotExist
>>>>>>> a0896c2174ea462ef2b0a72a7e51fccaecfd71b2

# from app.models import Article
from app.models import Profile, Question, Tag, Answer
from app.models import VoteForAnswer, VoteForQuestion

<<<<<<< HEAD
def paginate(content_list, request, num_per_page):
    paginator = Paginator(content_list, num_per_page)

    page = request.GET.get("page")
    content_list = paginator.get_page(page)
    return content_list

def index(request):
    questions = Question.objects.new_questions()
    content = paginate(questions, request, 5)
    return render(request, 'index.html', {'content': content})
=======
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
>>>>>>> a0896c2174ea462ef2b0a72a7e51fccaecfd71b2

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

<<<<<<< HEAD
def settings(request):
    return render(request, 'settings.html', {})
=======

def login(request):
    return render(request, 'login.html')
>>>>>>> a0896c2174ea462ef2b0a72a7e51fccaecfd71b2


def signup(request):
    return render(request, 'signup.html')


<<<<<<< HEAD
def hot(request):
    questions = Question.objects.hot_questions()
    content = paginate(questions, request, 5)
    return render(request, 'index.html', {'content': content})


def tag(request, tag_name):
    questions = Question.objects.tag_questions(tag_name)
    content = paginate(questions, request, 5)
    return render(request, 'tag.html', {'content': content, 'tag_name': tag_name})


def question(request, pk):
    # .select_related() не работает
    selected_question = Question.objects.single_question(pk)
    selected_answers = Answer.objects.filter(question=selected_question)
    content = paginate(selected_answers, request, 3)
    return render(request, 'question.html', {'question': selected_question, 'content': content})
=======
def settings(request):
    return render(request, 'settings.html')
>>>>>>> a0896c2174ea462ef2b0a72a7e51fccaecfd71b2
