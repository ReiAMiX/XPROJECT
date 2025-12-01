from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'  # название таблицы в единственном числе
        verbose_name_plural = 'Категории'  # название таблицы во множественном числе


"""Category
create table category(
    name varchar(100)
);

create table post(
category_id integer,
foreign key (category_id) references category(id)
);
"""


class Post(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    short_description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание', null=True, blank=True)
    views_qty = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    preview = models.ImageField(upload_to='posts/previews/', verbose_name='Заставка', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='posts')

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'post_id': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['id']


# создать таблицу FAQ
# question - charfield
# answer - textfield

# создать таблицу Comment
# text - textfield
# author - foreingkey
# created_at - datetimefield


class FAQ(models.Model):
    question = models.CharField(max_length=100)
    answer = models.TextField(max_length=100)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Вопросы-ответы'


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class PostPhoto(models.Model):
    photo = models.ImageField(upload_to='posts/photos/', verbose_name='Фото')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост', related_name='photos')


class PostViewsCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Like(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ManyToManyField(User, related_name='likes')


class Dislike(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ManyToManyField(User, related_name='dislikes')