from django.db import models


class Comments(models.Model):
    comment_author = models.CharField(max_length=128, verbose_name='Имя автора коментария')
    comment_text = models.TextField('Текст коментария')

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return self.comment_author


class Access_token(models.Model):
    access_token = models.TextField('Access Token')
    class Meta:
        verbose_name = 'Access token'


    def __str__(self):
        return self.access_token

class Refresh_token(models.Model):
    refresh_token = models.TextField('Refresh Token')
    class Meta:
        verbose_name = 'Refresh token'

    def __str__(self):
        return self.refresh_token



