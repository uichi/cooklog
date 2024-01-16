from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, introduction=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username,
            email=self.normalize_email(email),
            introduction=introduction
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, introduction=None):
        user = self.create_user(
            username,
            password=password,
            introduction=introduction
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField('ユーザー名', max_length=16, null=False)
    image = models.ImageField('プロフィール画像', upload_to='profile_images', null=True)
    email = models.EmailField('メールアドレス', max_length=255, unique=True)
    introduction = models.CharField('自己紹介', max_length=128, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        return self.is_admin
