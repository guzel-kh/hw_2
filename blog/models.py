from django.db import models

NULLABLE = {'null': 'True', 'blank': 'True'}


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='название поста')
    slug = models.CharField(max_length=200, verbose_name='slug')
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blog/', verbose_name='превью', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
