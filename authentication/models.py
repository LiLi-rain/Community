from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    """用户映射类
    """
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    gender = models.BooleanField(null=True)
    is_admin = models.BooleanField(default=False)  # 默认不是超级权限管理员
    is_staff = models.BooleanField(default=False)  # 默认不是协管员
    is_active = models.BooleanField(default=True)  # 默认是活动用户

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_userid(self):
        return self.__class__.objects.get(username=self.username).user_id

    def __repr__(self):
        return f'<User: {self.username or "Nobody"}>'
