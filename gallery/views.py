import re
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.urls import reverse
from gallery.models import UserProfile
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
            login(request,user)     # 记录用户登录状态（某些页面只有登录才能进行访问）
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
            return render(request, "login.html", {'errmsg': '用户名或密码错误'})    # 不合法


# 注册
class RegisterView(View):
    def get(self, request):
        """显示注册页面"""
        return render(request, "register.html")

    def post(self, request):
        """处理用户注册数据"""
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        password2 = request.POST.get("cpwd")
        email = request.POST.get("email")
        allow = request.POST.get("allow")
        # 校验数据
        if not all([username, password, password2, email]):
            return render(request, "register.html", {"error_msg": "注册信息不完整"})
        if not re.match(r"^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
            return render(request, "register.html", {"error_msg": "邮箱格式不正确"})
        if password != password2:
            return render(request, "register.html", {"error_msg": "两次输入的密码不一致"})
        if allow != "on":
            return render(request, "register.html", {"error_msg": "请勾选同意"})
        # 数据库查询是否已注册（用户名重复）
        try:
            user = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            # 用户未注册，可用
            user = None
        if user:
            # 已注册
            return render(request, "register.html", {"error_msg": "用户名已存在"})
        # 存储用户信息
        user = UserProfile.objects.create_user(username, email, password)
        user.is_active = 0  # 关闭自动激活
        user.save()         # 保存信息
        # 返回应答
        return redirect(reverse("goods:index"))






