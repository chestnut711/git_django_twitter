from django.db.models import Q
from django.shortcuts import render
from .models import Post
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required



def index(request):
    """投稿一覧ページ"""

    # ログイン時のみ投稿を表示
    if request.user.is_authenticated:
        user = request.user
        followees = user.followees.all()
        posts = Post.objects.filter(
            Q(user=user) |
            Q(user__in=followees)
        ).order_by('-id').distinct()
    else:
        posts = None
    context = {
        'posts': posts,
    }
    return render(request, 'app/index.html', context)


@require_POST
def users_follow(request, pk):
    """フォロー機能"""
    login_user = request.user
    user = get_object_or_404(get_user_model(), pk=pk)
    followees = login_user.followees.all()
    #既にフォローしていれば解除、していなければフォロー
    if user in followees:
        login_user.followees.remove(user)
        messages.success(request, 'フォローを解除しました')
    else:
        login_user.followees.add(user)
        messages.success(request, 'フォローしました')
    return redirect('app:users_detail', pk=pk)


@login_required
def users_followlist(request, pk):
    """フォロー一覧画面"""
    user = get_object_or_404(get_user_model(), pk=pk)
    #フォローしているユーザー
    followees = user.followees.all()
    #フォローされているユーザー
    followers = get_user_model().objects.filter(followees=user)
    context = {
        'user': user,
        'followees': followees,
        'followers': followers,
    }
    return render(request, 'app/users_followlist.html', context)
