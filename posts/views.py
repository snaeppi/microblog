from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from .models import Post, User


def get_posts_for_query(query):
    if query:
        posts = Post.objects.filter(content__icontains=query)
    else:
        posts = Post.objects.all()

    return posts


@login_required
def create_post(request):
    content = request.POST.get('content')

    if not content:
        raise ValidationError("Post content cannot be empty.")
    if len(content) > 280:
        raise ValidationError("Post content exceeds the maximum length of 280 characters.")
    
    Post.objects.create(author=request.user, content=content, length=len(content))


@login_required
def home(request):
    context = {}

    if request.method == 'POST':
        try:
            create_post(request)
        except ValidationError as e:
            context['error'] = e.message

    query = request.GET.get('q', '')
    context['posts'] = get_posts_for_query(query)
    context['query'] = query

    return render(request, 'home.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user.is_superuser or request.user == post.author:
        post.delete()
    return redirect('/')


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
         return redirect('/')
    
    if request.method == 'POST':
        post.content = request.POST.get('content')
        post.length = len(post.content)
        post.save()
        return redirect('/')
    return render(request, 'edit_post.html', {'post': post})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
