from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model  # 사용자가 데이터 베이스 안에 있는지 검사
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return  redirect('/')
        else:
            return render(request, 'signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        email = request.POST.get('email', None)

        if password != password2:
            return render(request, 'signup.html')
        else:
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'signup.html')
            else:
                UserModel.objects.create_user(username=username, password=password, email=email)
            return redirect('/user-login')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        me = auth.authenticate(request, username=username, password=password)
        if me is not None:  # 저장된 사용자의 패스워드와 입력받은 패스워드 비교
            auth.login(request, me)
            return redirect('/')
        else:   # 로그인이 실패하면 다시 로그인 페이지를 보여주기
            return redirect('/user-login')
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'userlogin.html')

@login_required
def user_logout(request):
    auth.logout(request)
    return redirect('/')



