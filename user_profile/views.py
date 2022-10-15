from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView

from authentication.models import User
from .models import Profile

@method_decorator([login_required], name='dispatch')
class ProfileDetailView(TemplateView):
    """展示用户详情页面的视图类
    """

    model = Profile
    template_name = 'user_profile/profile.html'

    def get_context_data(self, **kwargs):
        """给模板文件传递键值对
        """
        # 此时 context 字典中有俩数据：{'user_id': 用户ID, 'view': 视图类实例}
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        # 这个 self.kwargs 是解析请求路径时得到的
        user_id = self.kwargs.get('user_id')
        context['user_'] = User.objects.get(id=user_id)
        context['profile'] = Profile.objects.get(user_id=user_id)
        return context


@method_decorator([login_required], name='dispatch')
class UpdateProfileView(UpdateView):
    """更新用户详情的视图类
    """

    model = Profile
    # UpdateView 的父类 ModelFormMixin 的 get_form_class 方法用到了 fields 属性
    # 此方法的返回值是 django.forms.models 模块中 modelform_factory 函数的调用
    # modelform_factory 的返回值是一个根据 fields 属性创建的表单类
    # 也就是说 get_form_class 方法的返回值是利用 fields 创建的表单类
    fields = ['avatar', 'url', 'location', 'job']
    template_name = 'user_profile/profile_update.html'

    def dispatch(self, request, *args, **kwargs):
        # 这里加个判断
        # 如果当前登录的用户不是超级用户且与被编辑的用户不是同一个
        # 则重定向到被编辑的用户的详情页
        if (not request.user.is_admin and
                request.user.id != kwargs.get('user_id')):
            return redirect('user_profile:profile', self.kwargs.get('user_id'))
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return Profile.objects.get(user_id=self.kwargs.get('user_id'))

    def get_context_data(self, **kwargs):
        kw = super().get_context_data(**kwargs)
        kw['user_'] = User.objects.get(id=self.kwargs.get('user_id'))
        return kw

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.save()
        form.save_m2m()