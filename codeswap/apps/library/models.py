from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


class ProgrammingLanguage(models.Model):
    """
    Model for programming languages.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True)
    icon_class = models.CharField(max_length=50, blank=True, verbose_name='CSS класс иконки')
    
    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """
    Model for code tags.
    """
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True)
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class CodeSnippet(models.Model):
    """
    Model for code snippets.
    """
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippets', verbose_name='Автор')
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, related_name='snippets', verbose_name='Язык')
    code = models.TextField(verbose_name='Код')
    description = models.TextField(verbose_name='Описание')
    tags = models.ManyToManyField(Tag, blank=True, related_name='snippets', verbose_name='Теги')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    likes_count = models.PositiveIntegerField(default=0, verbose_name='Лайки')
    downloads_count = models.PositiveIntegerField(default=0, verbose_name='Скачивания')
    
    class Meta:
        verbose_name = 'Сниппет кода'
        verbose_name_plural = 'Сниппеты кода'
        ordering = ['-created_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('library:snippet_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Создаем slug из заголовка
            slug = slugify(self.title)
            
            # Если slug пустой (например, если название на кириллице), добавляем id или метку времени
            if not slug:
                # Если у объекта уже есть id, используем его
                if self.id:
                    slug = f"snippet-{self.id}"
                else:
                    # Иначе используем временную метку
                    slug = f"snippet-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            
            # Проверяем уникальность slug
            counter = 1
            original_slug = slug
            while CodeSnippet.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
                
            self.slug = slug
            
        super().save(*args, **kwargs)


class Comment(models.Model):
    """
    Model for snippet comments.
    """
    snippet = models.ForeignKey(CodeSnippet, on_delete=models.CASCADE, related_name='comments', verbose_name='Сниппет')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_date']
    
    def __str__(self):
        return f'Комментарий от {self.author.username} к {self.snippet.title}'


class Like(models.Model):
    """
    Model for snippet likes.
    """
    snippet = models.ForeignKey(CodeSnippet, on_delete=models.CASCADE, related_name='likes', verbose_name='Сниппет')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='Пользователь')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    
    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('snippet', 'user')
    
    def __str__(self):
        return f'Лайк от {self.user.username} к {self.snippet.title}' 