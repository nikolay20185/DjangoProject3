<picture>
 <source media="(prefers-color-scheme: dark)" srcset="[![2025-04-18-21-36-34.png](https://i.postimg.cc/43Px0fPz/2025-04-18-21-36-34.png)](https://postimg.cc/1ggSnZLt)">
 <source media="(prefers-color-scheme: light)" srcset="[![2025-04-18-21-36-34.png](https://i.postimg.cc/43Px0fPz/2025-04-18-21-36-34.png)](https://postimg.cc/1ggSnZLt)">
 <img alt="https://i.postimg.cc/43Px0fPz/2025-04-18-21-36-34.png" src="https://i.postimg.cc/43Px0fPz/2025-04-18-21-36-34.png">
</picture>



# CodeSwap - платформа обмена кодом для Cursor IDE

CodeSwap - это веб-приложение на Django, предназначенное для обмена кодом и его фрагментами между разработчиками, использующими Cursor IDE. Платформа позволяет пользователям находить готовые решения, делиться своим кодом и общаться с другими разработчиками.

## Основные возможности

- **Библиотека кода**: Поиск, просмотр и публикация сниппетов кода
- **Авторизация**: Регистрация и аутентификация пользователей
- **Сообщество**: Форум для обсуждения вопросов разработки
- **Интеграция с Cursor IDE**: Возможность импортировать код напрямую в IDE

## Технический стек

- **Backend**: Python/Django
- **Frontend**: HTML, TailwindCSS, JavaScript
- **База данных**: SQLite (для разработки)
- **Хранение изображений**: Django File Storage с Pillow

## Установка

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/yourusername/codeswap.git
   cd codeswap
   ```

2. Создайте и активируйте виртуальное окружение:
   ```
   python -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   ```

3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

4. Выполните миграции:
   ```
   python manage.py migrate
   ```

5. Создайте суперпользователя:
   ```
   python manage.py createsuperuser
   ```

6. Запустите сервер:
   ```
   python manage.py runserver
   ```

7. Откройте сайт в браузере: http://127.0.0.1:8000/

## Структура проекта

- `codeswap/` - основная директория проекта
  - `apps/` - приложения проекта
    - `core/` - основное приложение (главная страница, общие вьюхи)
    - `accounts/` - авторизация и профили пользователей
    - `library/` - библиотека сниппетов кода
    - `community/` - форум и сообщество
  - `templates/` - шаблоны HTML
  - `static/` - статические файлы (CSS, JS, изображения)
  - `media/` - загружаемые пользователями файлы

## Лицензия

MIT License 
