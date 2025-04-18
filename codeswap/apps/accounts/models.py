from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    """
    User profile model that extends the built-in User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profile_avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, verbose_name='О себе')
    github_url = models.URLField(blank=True, verbose_name='GitHub профиль')
    website = models.URLField(blank=True, verbose_name='Персональный сайт')
    specialization = models.CharField(max_length=100, blank=True, verbose_name='Специализация')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        
    def __str__(self):
        return f'Профиль {self.user.username}'
    
    def get_absolute_url(self):
        return reverse('accounts:profile_detail', kwargs={'username': self.user.username}) 