from django.db import models
from django.utils.translation import gettext_lazy as _
from .settings import TransactionType


class Transaction(models.Model):
    class Meta:
        db_table = 'point'

    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=False, related_name='transactions')
    type = models.CharField(_('type'), choices=TransactionType.choices(), null=False, max_length=50)
    value = models.DecimalField(_('value'), decimal_places=0, max_digits=20, null=False)
    date = models.DateTimeField(_('date'), auto_now_add=True)
    description = models.TextField(_('description'), null=True, blank=True)

