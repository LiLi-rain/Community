from django.db import models
from django.db.models.signals import post_save

from authentication.models import User


# 父类是 django.db.models.base.Model 类
class Profile(models.Model):
    """用户个人简介映射类
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    job = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.ImageField(upload_to='pic_folder', default='img/user.png')
    class Meta:
        db_table = 'user_profile'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)