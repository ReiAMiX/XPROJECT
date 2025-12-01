from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category, Post, Comment, Like, Dislike, PostViewsCount
from django.core.paginator import Paginator
from .forms import LoginForm, RegisterForm, CommentForm, PostForm
from django.contrib.auth import login, logout
from django.views.generic import UpdateView, DeleteView

# Create your views here.


class UpdatePost(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'main/create_post.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = 'Обновить пост'
        context['page_button'] = 'Обновить'
        return context


class DeletePost(DeleteView):
    model = Post
    template_name = 'main/post_confirm_delete.html'
    pk_url_kwarg = 'post_id'
    success_url = '/'

# posts/<int:post_id>/update/
def show_home_page(request):
    # select * from categories
    posts = Post.objects.all()
    for post in posts:
        try:
            post.likes
        except Exception as e:
            Like.objects.create(post=post)

        try:
            post.dislikes
        except Exception as e:
            Dislike.objects.create(post=post)

    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts
    }
    return render(request, 'main/index.html', context)


def show_contacts_page(request):
    return render(request, 'main/contacts.html')


def show_faq_page(request):
    return render(request, 'main/faq.html')


def show_create_post_page(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # AnonymousUser
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('post-detail', form.id)
    else:
        form = PostForm()

    page_title = 'Создать пост'
    page_button = 'Создать'

    context = {
        'form': form,
        'page_title': page_title,
        'page_button': page_button
    }
    return render(request, 'main/create_post.html', context)

# переход на страницу faq frequently asked question


def show_registration_page(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()  # отправляем данные в БД
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'form': form
    }
    return render(request, 'main/registration.html', context)


def show_login_page(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # получаем пользователя с базы данных
            if user is not None:  # если пользователь найден, то заходим в его аккаунт
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'main/login.html', context)


def show_category_articles_page(request, category_id):
    sort = request.GET.get('sort', 'id')

    posts = Post.objects.filter(category__id=category_id).order_by(sort)


    sorting_fields = {
        'По дате': ['created_at', '-created_at'],
        'По просмотрам': ['views_qty', '-views_qty'],
        'По названию': ['name', '-name']
    }
    context = {
        'posts': posts,
        'sorting_fields': sorting_fields
    }
    return render(request, 'main/category_articles.html', context)


def show_post_page(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.post = post
            form.save()
            return redirect('post-detail', post_id)
    else:
        form = CommentForm()

    comments = Comment.objects.filter(post=post)

    if request.user.is_authenticated:
        viewed_post, is_created = PostViewsCount.objects.get_or_create(
            post=post,
            user=request.user,
        )
        if is_created:
            post.views_qty += 1
            post.save()

    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request, 'main/post_detail.html', context)

# отобразить на детальной странице все комментарии статьи

def user_logout(request):
    logout(request)
    return redirect('home')


def delete_post_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    post_id = comment.post.id
    comment.delete()
    return redirect('post-detail', post_id)


from django.contrib.auth.models import User


def show_author_profile_page(request, username):
    user = User.objects.get(username=username)

    posts = Post.objects.filter(author=user)

    total_comments = [post.comment_set.all().count() for post in posts]
    total_likes = [post.likes.user.all().count() for post in posts]
    total_dislikes = [post.dislikes.user.all().count() for post in posts]
    total_views = [post.views_qty for post in posts]

    context = {
        'user': user,
        'posts': posts,
        'total_comments': sum(total_comments),
        'total_likes': sum(total_likes),
        'total_dislikes': sum(total_dislikes),
        'total_views': sum(total_views)
    }
    return render(request, 'main/author_profile.html', context)


def add_like_or_dislike(request, post_id, action):
    post = Post.objects.get(id=post_id)

    if action == 'add_like':
        if request.user in post.likes.user.all():
            post.likes.user.remove(request.user.id)
        else:
            post.likes.user.add(request.user.id)
            post.dislikes.user.remove(request.user.id)
    elif action == 'add_dislike':
        if request.user in post.dislikes.user.all():
            post.dislikes.user.remove(request.user.id)
        else:
            post.dislikes.user.add(request.user.id)
            post.likes.user.remove(request.user.id)

    return redirect('post-detail', post_id)


def search(request):
    query = request.GET.get('q')

    if not query:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(name__iregex=query)

    context = {
        'posts': posts
    }
    return render(request, 'main/search_page.html', context)
