from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from django.utils import timezone
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .utils import censor_text  # 맨 위에 추가
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

ADMIN_USERS = ['sm102kg', 'sm갈통', 'smile', 'smplay']

def index(request):
    board = request.GET.get('board', '전체')
    sort = request.GET.get('sort', 'created_at')  # ✅ 기본값 수정

    if board == '전체':
        posts = Post.objects.exclude(category__in=['1학년 둥지', '2학년 둥지', '3학년 둥지']) 
    else:
        posts = Post.objects.filter(category=board)

    # ✅ 정렬 조건 처리
    if sort == 'likes':
        posts = posts.order_by('-like_count')
    elif sort == 'views':
        posts = posts.order_by('-view_count')
    elif sort == 'created_at':
        posts = posts.order_by('-created_at')
    else:
        posts = posts.order_by('-created_at')

    # 댓글 수 미리 계산
    for post in posts:
        post.comment_count = post.comments.count()

    user_count = User.objects.count()
    tab_list = ['전체', '자유', '공지', '1학년 둥지', '2학년 둥지', '3학년 둥지']

    return render(request, 'board/index.html', {
        'posts': posts,
        'board': board,
        'user_count': user_count,
        'ADMIN_USERS': ADMIN_USERS,
        'tab_list': tab_list,
        'sort': sort,  # ✅ 템플릿에서 선택 유지용
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.view_count += 1
    post.save()

    comments = Comment.objects.filter(post=post)

    return render(request, 'board/post_detail.html', {
        'post': post,
        'comments': comments,
        'ADMIN_USERS': ADMIN_USERS,
    })


@login_required
@login_required
def create_post(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        if not category:
            messages.error(request, '말머리를 선택해 주세요.')
            return redirect('create_post')

        # 공지글 제한
        if category == '공지' and request.user.username not in ADMIN_USERS:
            messages.error(request, '공지글은 관리자만 작성할 수 있습니다.')
            return redirect('create_post')

        Post.objects.create(
            title=censor_text(request.POST.get('title')),
            content=censor_text(request.POST.get('content')),
            writer=request.user.username,
            category=category,
            file=request.FILES.get('file')
        )
        return redirect('index')

    return render(request, 'board/create_post.html', {'ADMIN_USERS': ADMIN_USERS})


@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        Comment.objects.create(
            post_id=post_id,
            writer=request.user.username,
            content=censor_text(request.POST['content']),
        )
    return redirect('post_detail', post_id=post_id)


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    liked_posts = request.session.get('liked_posts', [])
    if post_id not in liked_posts:
        post.like_count += 1
        post.save()
        liked_posts.append(post_id)
        request.session['liked_posts'] = liked_posts
    return redirect('post_detail', post_id=post_id)


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        if request.user.username in ADMIN_USERS or post.writer == request.user.username:
            post.delete()
            messages.success(request, '게시물이 삭제되었습니다.')
        else:
            messages.error(request, '삭제 권한이 없습니다.')
        return redirect('index')
    return redirect('post_detail', post_id=post_id)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'board/signup.html', {'form': form})
@login_required
def report_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.report_count += 1
    post.save()
    messages.success(request, "해당 게시글을 신고했습니다.")
    return redirect('post_detail', post_id=post_id)

@login_required
def reported_posts(request):
    if request.user.username not in ADMIN_USERS:
        messages.error(request, "접근 권한이 없습니다.")
        return redirect('index')

    posts = Post.objects.filter(report_count__gte=1)  # ✅ 신고된 글만 필터링

    return render(request, 'board/reported_posts.html', {
        'reported_posts': posts
    })

