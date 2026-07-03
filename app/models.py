from django.db import models


class Comments(models.Model):
    comment_author = models.CharField(max_length=128, verbose_name='Имя автора коментария')
    comment_text = models.TextField('Текст коментария')

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return self.comment_author


