from .models import Article
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})


def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404


def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
            if form["text"] and form["title"]:
                coincidence = False
                for article in Article.objects.all():
                    if article.title == form["title"]:
                        coincidence = True
                if coincidence:
                    form['errors'] = u"Название статьи уже существует"
                    return render(request, 'create_post.html', {'form': form})
                article = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                return redirect('get_article', article_id=article.id)
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            return render(request, 'create_post.html', {})
    else:
        raise Http404


def register(request):
    if not request.user.is_anonymous:
        return archive(request)
    else:
        if request.method == "POST":
            form = {
                'login': request.POST["login"], 'email': request.POST["email"], 'password': request.POST["password"]
            }
            if form["login"] and form["email"] and form["password"]:
                try:
                    User.objects.get(username=form["login"])
                    form['errors'] = u"Пользователь с таким именем уже есть"
                    return render(request, 'register.html', {'form': form})
                except User.DoesNotExist:
                    User.objects.create_user(form["login"], form["email"], form["password"])
                    return redirect('archive')
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'register.html', {'form': form})
        else:
            return render(request, 'register.html', {})


def login_user(request):
    if not request.user.is_anonymous:
        return archive(request)
    else:
        if request.method == "POST":
            form = {
                'login': request.POST["login"], 'password': request.POST["password"]
            }
            if form["login"] and form["password"]:
                user = authenticate(request, username=form["login"], password=form["password"])
                if user is not None:
                    login(request, user)
                    return redirect('archive')
                else:
                    form['errors'] = u"Пользователя с таким набором логина и пароля не существует"
                    return render(request, 'login.html', {'form': form})
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {})
