from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from datetime import date
from datetime import datetime
from django.http import JsonResponse
from django.db.models import F

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from .forms import *

from app.models import Profile, Question, Tag, Answer
from app.models import VoteForAnswer, VoteForQuestion

from app.forms import LoginForm

def paginate(content_list, request, num_per_page):
    paginator = Paginator(content_list, num_per_page)

    page = request.GET.get("page")
    content_list = paginator.get_page(page)
    return content_list

def index(request):
    questions = Question.objects.new_questions()
    content = paginate(questions, request, 5)
    return render(request, 'index.html', {'content': content})

@login_required(login_url='/login/')
def settings(request):
    if request.method == 'POST':
        user = request.user
        form = SettingsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            if form.cleaned_data['username']:
                user.username = form.cleaned_data['username']
            if form.cleaned_data['email']:
                user.email = form.cleaned_data['email']
            user.save()

            new_profile = Profile.objects.get(user=request.user)

            if form.cleaned_data['avatar']:
                new_profile.avatar = form.cleaned_data['avatar']
            new_profile.save()
            return redirect(reverse('settings'))
    else:
        form = SettingsForm()
    return render(request, 'settings.html', {
        'form': form,
    }
                  )

def login(request):
    redirect_to = request.GET.get('next', '/')
    error_message = None
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(redirect_to)
            else:
                error_message = "Sorry, wrong login or password"
    return render(request, 'login.html', {'form': form, 'redirect_to': redirect_to, 'error_message': error_message})

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('next', '/'))


def signup(request):
    error = []
    if request.method == 'POST':
        form = SignUpForm(data=request.POST, auto_id=False)
        if form.is_valid():
            new_user = form.save()
            new_user.username= form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            auth.login(request, new_user)
            return redirect(reverse('index'))

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {
        'error': error,
        'form': form
    }
                  )


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

    if request.method == "GET":
        form = AnswerForm()

    if request.method == "POST":
        form = AnswerForm(data=request.POST)
        profile = Profile.objects.filter(user=request.user).values("id")
        if form.is_valid():
            answer = Answer.objects.create(question_id=selected_question.id,
                                           author_id=profile,
                                           text=form.cleaned_data["text"])
            return redirect(reverse("question", kwargs={"pk": selected_question.id}) + "?page="
                            + str(content.paginator.num_pages+1))

    return render(request, "question.html",
                  {"question": selected_question, "content": content, "form": form})

@login_required(login_url='/login/')
def ask(request):

    if request.method == "GET":
        form = AskForm()

    if request.method == "POST":
        form = AskForm(data=request.POST)
        if form.is_valid():
            tags = form.save()
            profile = Profile.objects.filter(user=request.user).values("id")
            question = Question.objects.create(author_id=profile,
                                               title=form.cleaned_data["title"],
                                               text=form.cleaned_data["text"],
                                               date=datetime.today())
            for _tag in tags:
                question.tags.add(_tag)
                question.save()
            return redirect("question", pk=question.id)
    return render(request, "ask.html", {"form": form})

@login_required
@require_POST
def vote(request):
    data = request.POST
    return JsonResponse(data)
