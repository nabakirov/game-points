from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .settings import PROFILE_UPLOAD_DIR


class User(AbstractBaseUser):
    class Meta:
        db_table = 'user'
    USERNAME_FIELD = 'username'

    username = models.CharField(_('username'), max_length=50, null=False, blank=False, unique=True)
    interests = models.TextField(_('interests'), null=True, blank=True)
    date_joined = models.DateTimeField(_('registration date'), auto_now_add=True)
    is_active = models.BooleanField(_('is active'), default=True)
    is_superuser = models.BooleanField(_('is superuser'), default=False)
    password = models.CharField(_('password'), max_length=128, null=False, blank=False)
    photo = models.ImageField(_('photo'), upload_to=PROFILE_UPLOAD_DIR, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.photo_ = self.photo

    def __str__(self):
        return f'{self.username}'


