from .celery import app as celery_app
import sys


sys.set_int_max_str_digits(0)


__all__ = ('celery_app',)