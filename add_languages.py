import os
import django
import sys

# Настройка Django
sys.path.append('.')  # Добавляем текущую директорию в путь
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codeswap.settings')
django.setup()

from django.utils.text import slugify
from codeswap.apps.library.models import ProgrammingLanguage

# Список языков программирования для добавления
LANGUAGES = [
    {"name": "Python", "icon_class": "fab fa-python"},
    {"name": "JavaScript", "icon_class": "fab fa-js"},
    {"name": "HTML", "icon_class": "fab fa-html5"},
    {"name": "CSS", "icon_class": "fab fa-css3-alt"},
    {"name": "Java", "icon_class": "fab fa-java"},
    {"name": "C++", "icon_class": "fas fa-code"},
    {"name": "C#", "icon_class": "fab fa-microsoft"},
    {"name": "PHP", "icon_class": "fab fa-php"},
    {"name": "Ruby", "icon_class": "fas fa-gem"},
    {"name": "Swift", "icon_class": "fab fa-swift"},
    {"name": "TypeScript", "icon_class": "fab fa-js"},
    {"name": "Go", "icon_class": "fas fa-code"},
    {"name": "Rust", "icon_class": "fas fa-cog"},
    {"name": "Kotlin", "icon_class": "fab fa-android"},
    {"name": "SQL", "icon_class": "fas fa-database"},
    {"name": "Shell", "icon_class": "fas fa-terminal"},
    {"name": "Markdown", "icon_class": "fas fa-file-alt"},
]

def add_languages():
    languages_added = 0
    languages_updated = 0
    
    for lang_data in LANGUAGES:
        # Создаем slug из имени языка
        slug = slugify(lang_data["name"])
        
        # Пытаемся найти существующий язык или создаем новый
        try:
            lang = ProgrammingLanguage.objects.get(slug=slug)
            # Обновляем существующий язык
            lang.name = lang_data["name"]
            lang.icon_class = lang_data["icon_class"]
            lang.save()
            languages_updated += 1
            print(f"Обновлен существующий язык: {lang.name}")
        except ProgrammingLanguage.DoesNotExist:
            # Создаем новый язык
            lang = ProgrammingLanguage.objects.create(
                name=lang_data["name"],
                slug=slug,
                icon_class=lang_data["icon_class"]
            )
            languages_added += 1
            print(f"Добавлен новый язык: {lang.name}")
    
    print(f"\nИтого: добавлено {languages_added}, обновлено {languages_updated} языков.")

if __name__ == "__main__":
    print("Добавление языков программирования в базу данных...")
    add_languages()
    print("Готово!") 