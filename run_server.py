import subprocess
import sys

try:
    # Выполняем команду migrate
    print("Запуск миграций...")
    subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
    
    # Запускаем сервер
    print("Запуск сервера...")
    subprocess.run([sys.executable, "manage.py", "runserver"])
except subprocess.CalledProcessError as e:
    print(f"Произошла ошибка: {e}")
except Exception as e:
    print(f"Неожиданная ошибка: {e}") 