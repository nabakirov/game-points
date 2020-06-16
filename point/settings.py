from django.utils.translation import gettext_lazy as _


class TransactionType:
    add = 'add'
    exchange = 'exchange'

    @classmethod
    def choices(cls):
        return (
            (cls.add, _(cls.add)),
            (cls.exchange, _(cls.exchange))
        )
