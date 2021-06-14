import random

from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from random import sample, choice
questions = [
    {
        'id': idx,
        'title': f'Title number {idx}',
        'text': f'Some text for question #{idx}'
    } for idx in range(10)
]

answers = [
    {
        'id': idx_ans,
        'title': f'Answer number {idx_ans}',
        'text': f'Some text for question #{idx_ans}'
    } for idx_ans in range(5)
]

list_all_tags = ['Perl', 'Python', 'TechnoPark', 'MYSQL', 'django', 'Mail.ru', 'Voloshin', 'Firefox']


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(questions, 5)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    question = paginate(questions, request)
    return render(request, 'index.html', {'questions': question, "tags": sample(list_all_tags, 2)})


def ask(request):
    return render(request, 'ask.html', {})


def login(request):
    return render(request, 'login.html', {})


def question(request, pk):
     question = questions[pk]
     return render(request, "question.html", {"question": question, "answers": answers,
                                              "tags": sample(list_all_tags, 2)})


def signup(request):
    return render(request, 'signup.html', {})


def settings(request):
    return render(request, 'settings.html', {})


def tag(request, tag):
    question = paginate(questions, request)
    return render(request, 'tag.html', {'questions': question, "tags": [tag, random.choice(list_all_tags)], "tag": tag})
