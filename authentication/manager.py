from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, email, password, gender=None, **kwargs):
        """创建普通用户的方法"""
        # 邮箱和用户名必须存在
        if not email or not username:
            raise ValueError("Users must have avalid email and username.")

        # 该类实例化时，一定会将实例赋值给某个映射类的 objects 属性
        # self.model 的值就是映射类本身
        # 下面的代码的作用是创建映射类的实例并赋值给变量 user
        user = self.model(
            username = username,
            # self.normalize_email 是在 BaseUserManager 类中定义的类方法
            # 该方法用于格式化邮箱
            email = self.normalize_email(email),
        )
        # 创建映射类通常需要继承 django.db.models 模块中的 Model 类
        # AbstractBaseUser 是 Model 的子类
        # set_password 方法是在 AbstractBaseUser 类中定义的
        # 如果映射类将当前所在类 UserManager 的实例赋值给属性 objects
        # 那么映射类在创建时一定会继承 AbstractBaseUser 类
        # 所以 user 变量作为映射类的实例，自然就有了 set_password 方法
        # set_password 的源码在 django.contrib.auth.base_user 模块中
        # 该方法的作用是对密码进行哈希加密，并保存原密码值
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, **kwargs):
        """创建超级用户的方法"""

        user = self.create_user(
            username, email, password, **kwargs
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user