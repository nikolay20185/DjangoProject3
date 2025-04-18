import os
import sys

# Добавление текущего каталога в путь Python
sys.path.insert(0, os.path.abspath('.'))

# Запуск Django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codeswap.settings")
    execute_from_command_line(["manage.py", "migrate"]) 