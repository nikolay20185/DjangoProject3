from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Topic(models.Model):
    """
    Model for forum topics/categories.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(verbose_name='Описание')
    icon_class = models.CharField(max_length=50, blank=True, verbose_name='CSS класс иконки')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    
    class Meta:
        verbose_name = 'Тема форума'
        verbose_name_plural = 'Темы форума'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('community:topic_detail', kwargs={'slug': self.slug})


class Discussion(models.Model):
    """
    Model for forum discussions/threads.
    """
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='discussions', verbose_name='Тема')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions', verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_pinned = models.BooleanField(default=False, verbose_name='Закреплено')
    is_closed = models.BooleanField(default=False, verbose_name='Закрыто')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    
    class Meta:
        verbose_name = 'Обсуждение'
        verbose_name_plural = 'Обсуждения'
        ordering = ['-is_pinned', '-created_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('community:discussion_detail', kwargs={'slug': self.slug})
    
    @property
    def replies_count(self):
        return self.replies.count()
    
    @property
    def last_reply(self):
        return self.replies.order_by('-created_date').first()


class Reply(models.Model):
    """
    Model for discussion replies.
    """
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='replies', verbose_name='Обсуждение')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies', verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_solution = models.BooleanField(default=False, verbose_name='Помечено как решение')
    
    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['created_date']
    
    def __str__(self):
        return f'Ответ от {self.author.username} в {self.discussion.title}'


class Notification(models.Model):
    """
    Model for user notifications.
    """
    NOTIFICATION_TYPES = (
        ('reply', 'Новый ответ'),
        ('mention', 'Упоминание'),
        ('solution', 'Ответ отмечен как решение'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='Пользователь')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, verbose_name='Тип уведомления')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', verbose_name='Отправитель')
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications', verbose_name='Обсуждение')
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications', verbose_name='Ответ')
    message = models.TextField(verbose_name='Сообщение')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_date']
    
    def __str__(self):
        return f'Уведомление для {self.user.username}: {self.get_notification_type_display()}' 