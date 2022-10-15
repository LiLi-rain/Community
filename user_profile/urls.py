from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import ProfileDetailView, UpdateProfileView

app_name = 'user_profile'


urlpatterns = [
    # 此 path 函数的返回值是「路由处理对象」，即 URLResolver 类的实例
    path('user/',
        # 此 include 函数的返回值是一个三元元组，第一个元素是列表
        # 列表里面是两个「路由模式对象」，即 URLPattern 类的实例
        include(([
            path('<int:user_id>/', ProfileDetailView.as_view(), name='profile'),
            path('<int:user_id>/edit', UpdateProfileView.as_view(),
                name='update_profile'),
        ]))
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)