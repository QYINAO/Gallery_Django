from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.urls import reverse
# Create your views here.


# 登录
class LoginView(View):
    def get(self, request):
        # 判断是否记住用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        # register_form = RegisterFrom()
        return render(request, "login.html", {'username':username, 'checked':checked})

    def post(self, request):
        # 接受数据
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        # 数据合法判断
        if not all([username,password]):
            return render(request, "login.html", {'errmsg': '数据不完整'})
        # 登录校验
        user = authenticate(username=username,password=password)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                login(request,user)     # 记录用户登录状态（某些页面只有登录才能进行访问）
                # 获取登录后所要跳转的地址,
                # 默认跳转到首页
                next_url = request.GET.get('next', reverse('index'))

                # 跳转到next_url
                response = redirect(next_url)

                remember = request.POST.get('remember')     # 判断是否勾选了记住用户名

                if remember == "on":
                    # 记住用户名
                    response.set_cookie('username',username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')    # 未勾选记住用户名，删除cookie

                # 返回response
                return response
            else:
                # 用户未激活
                return render(request, "login.html", {'errmsg': '用户未激活'})
        else:
            return render(request, "login.html", {'errmsg': '用户名或密码错误'})    # 不合法









