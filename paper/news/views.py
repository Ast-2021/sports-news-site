from django.shortcuts import render
from django.urls import reverse_lazy
from .models import *
from .forms import CreatePost, RegisterUserForm, CommentsForm
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.contrib.auth.forms import AuthenticationForm, UserChangeForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView

headers = [
    {'title': 'Главная', 'url_name': 'main'},
    {'title': 'Форум', 'url_name': 'main'},
    {'title': 'Контакты', 'url_name': 'main'},
]


def index(request):
    posts = Article.objects.all()
    cats = Categories.objects.all()
    cat_selected = None
    return render(request, 'news/index.html', {'posts': posts, 'headers': headers, 'categories': cats, 'cat_selected': cat_selected})

def article(request, post_pk):
    post = Article.objects.get(pk=post_pk)
    cats = Categories.objects.all()
    comments = Comments.objects.all()
    form_comment = CommentsForm()
    if request.POST:
        form_comment = CommentsForm(request.POST)
        print(1)
        if form_comment.is_valid():
            print(2)
            comment = form_comment.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

    return render(request, 'news/post.html', {'post': post, 'headers': headers, 'categories': cats, 'form_comment': form_comment, 'comments': comments})

def create_post(request):

    if not request.user.is_authenticated:
        return redirect('login')
    
    form = CreatePost()
    cats = Categories.objects.all()
    if request.POST:
        form = CreatePost(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            image = form.cleaned_data['image']
            category = form.cleaned_data['category']
            Article(title=title, text=text, image=image, author=request.user, category=category).save()
            return redirect('main')

    return render(request, 'news/create.html', {'form': form, 'headers': headers, 'cat_selected': None, 'categories': cats})

def delete_post(request, post_pk):
    Article.objects.get(pk=post_pk).delete()
    return redirect('main')

def update_post(request, post_pk):
    post = get_object_or_404(Article, pk=post_pk)
    form = CreatePost(instance=post)
    cats = Categories.objects.all()
    if request.method == 'POST':
        form = CreatePost(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('main')
    return render(request, 'news/update.html', {'form': form, 'post': post, 'headers': headers, 'cat_selected': None, 'categories': cats})

def categories(request, cat_slug):
    cat_selected = cat_slug
    cats = Categories.objects.all()
    cattt = Categories.objects.get(slug=cat_slug)
    posts = Article.objects.filter(category=cattt)
    return render(request, 'news/index.html', {'posts': posts, 'headers': headers, 'categories': cats, 'cat_selected':cat_selected})

def register_user(request):
    cats = Categories.objects.all()
    form = RegisterUserForm()
    if request.POST:
        if RegisterUserForm(request.POST).is_valid():
            RegisterUserForm(request.POST).save()
            return redirect('login')
    return render(request, 'news/register_user.html', {'headers': headers, 'categories': cats, 'form': form})

def login_user(request):
    cats = Categories.objects.all()
    form = AuthenticationForm()

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.success(request, 'error in username or password')
            return redirect('login')

    return render(request, 'news/login.html', {'headers': headers, 'categories': cats, 'form': form})

def logout_user(request):
    logout(request)
    return redirect('main')

def self_user_profile(request):
    cats = Categories.objects.all()
    
    return render(request, 'news/self_user_profile.html', {'headers': headers, 'categories': cats})

class UserEditView(UpdateView):
    form = UserChangeForm
    fields = ['username', 'first_name', 'last_name', 'email', 'image']
    template_name = 'news/edit_profile.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self):
        return self.request.user
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headers'] = headers
        context['categories'] = Categories.objects.all()
        return context
    
def user_profile(request, user_pk):
    cats = Categories.objects.all()
    user = User.objects.get(pk=user_pk)
    articles = Article.objects.filter(author=user)
    return render(request, 'news/user_profile.html', {'headers': headers, 'categories': cats, 'user': user, 'articles': articles})

def delete_comment(request, comment_pk):
    comment = Comments.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('main')

def new_func():
    return ...