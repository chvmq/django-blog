from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name='Название категории')

    def get_absolute_url(self):
        return reverse(viewname='category', kwargs={"category_id": self.pk})

    class Meta:
        # представление объектов
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    def __str__(self):
        # строковое представлени объекта, магический метод
        return self.title


class News(models.Model):
    title = models.CharField(max_length=50, verbose_name="Наименование")
    content = models.TextField(blank=True, verbose_name="Контент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='get_news')
    views = models.IntegerField(default=0)

    # def sayHello(self):
    #     return "hello from Model"

    def get_absolute_url(self):
        return reverse(viewname='view_news', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']
