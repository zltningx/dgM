
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None
    last_name = None

    email = models.EmailField('email address',
                              max_length=255,
                              unique=True,
                              blank=True)

    phone = models.CharField('电话', blank=True, max_length=32, null=False, default='')
    full_name = models.CharField('中文姓名', max_length=32, blank=True, null=False, default='')
    user_id = models.CharField('工号', unique=True, blank=True, max_length=32, null=False, default='')

    avatar = models.URLField('头像url', blank=True, max_length=256, null=False,
                             default='https://img1.doubanio.com/view/group_topic/large/public/p116915028.jpg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.email
