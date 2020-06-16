from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from .settings import PROFILE_UPLOAD_DIR


class UserManager(BaseUserManager):
    def create_superuser(self, username, password):
        user = self.model(username=username)
        user.set_password(password)
        user.is_superuser = True
        user.save()
        return user

    def create_user(self, username, password):
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractBaseUser):
    class Meta:
        db_table = 'user'
    USERNAME_FIELD = 'username'
    objects = UserManager()

    username = models.CharField(_('username'), max_length=50, null=False, blank=False, unique=True)
    interests = models.TextField(_('interests'), null=True, blank=True)
    date_joined = models.DateTimeField(_('registration date'), auto_now_add=True)
    is_active = models.BooleanField(_('is active'), default=True)
    is_superuser = models.BooleanField(_('is superuser'), default=False)
    password = models.CharField(_('password'), max_length=128, null=False, blank=False)
    photo = models.ImageField(_('photo'), upload_to=PROFILE_UPLOAD_DIR, null=True, blank=True)

    points = models.DecimalField(_('points'), default=0, max_digits=20, decimal_places=0)

    def __str__(self):
        return f'{self.username}'

    @property
    def is_staff(self):
        return self.is_superuser

    def has_module_perms(self, *args, **kwargs):
        return self.is_superuser

    def has_perm(self, *args, **kwargs):
        return self.is_superuser


