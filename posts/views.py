from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from .models import Post, User


def get_posts_for_query(query):
    if query:
        # Flaw: SQL Injection vulnerability
        # Query with:
        # nopostcontainsthisstring%' UNION SELECT id, id, username, password FROM posts_user WHERE '%'='
        with connection.cursor() as cursor:
            cursor.execute(f"""
            SELECT posts_post.id, posts_user.id, posts_user.username, posts_post.content
            FROM posts_post 
            INNER JOIN posts_user ON posts_post.author_id = posts_user.id 
            WHERE posts_post.content LIKE '%{query}%'
            """)
            return [{'id': row[0], 'author__id': row[1], 'author__username': row[2], 'content': row[3]} for row in cursor.fetchall()]
    else:
        return list(Post.objects.all().select_related('author').values('id', 'content', 'author__id', 'author__username'))


def create_post(request, user_id):
    content = request.POST.get('content')
    user = User.objects.get(id=user_id)
    Post.objects.create(author=user, content=content, length=len(content))


def home(request):
    user_id = request.session.get('user_id')
    context = {}

    if user_id:
        if request.method == 'POST':
            create_post(request, user_id)

        query = request.GET.get('q', '')
        context['posts'] = get_posts_for_query(query)
        context['username'] = User.objects.get(id=user_id).username
        context['query'] = query

        print(context)

    return render(request, 'home.html', context)


def delete_post(request, post_id):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        post = get_object_or_404(Post, id=post_id)
        if user.is_admin or user == post.author:
            post.delete()
    return redirect('home')


def edit_post(request, post_id):
    # Flaw: Broken access control, ownership of post not checked
    post = Post.objects.get(id=post_id)
    user_id = request.session.get('user_id')
    
    if user_id and request.method == 'POST':
        post.content = request.POST.get('content')
        post.length = len(post.content)
        post.save()
        return redirect('home')
    return render(request, 'edit_post.html', {'post': post})


def register(request):
    if request.method == 'POST':
        # Flaw: Allowing weak passwords
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Flaw: Storing password in plain text
        User.objects.create(username=username, password=password)
        return redirect('login')
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Flaw: SQL Injection vulnerability
        # Use the "password": 
        # ' OR username = 'admin' AND '1'='1
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM posts_user WHERE username = '{username}' AND password = '{password}'")
            user = cursor.fetchone()

        if user:
            request.session['user_id'] = user[0]
            request.session['username'] = user[1]
            request.session['is_admin'] = user[3]
            return redirect('home')
    return render(request, 'login.html')


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('home')
