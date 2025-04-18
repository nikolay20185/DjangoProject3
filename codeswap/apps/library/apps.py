from django.apps import AppConfig


class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'codeswap.apps.library'
    verbose_name = 'Библиотека кода' 