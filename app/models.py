from django.db import models



class House(models.Model):
    house_name = models.CharField(max_length=128, verbose_name='Название домика')
    house_description = models.TextField('Описание для домика')
    house_price = models.DecimalField(max_digits=25, decimal_places=2, verbose_name='Стоимость аренды в суммах')
    house_photo1 = models.ImageField(upload_to='media', default='', verbose_name='Фотография домика', null=True, blank=True)
    house_photo2 = models.ImageField(upload_to='media', default='', verbose_name='Фотография домика', null=True, blank=True)
    house_photo3 = models.ImageField(upload_to='media', default='', verbose_name='Фотография домика', null=True, blank=True)
    house_photo4 = models.ImageField(upload_to='media', default='', verbose_name='Фотография домика', null=True, blank=True)
    house_photo5 = models.ImageField(upload_to='media', default='', verbose_name='Фотография домика', null=True, blank=True)
    class Meta:
        verbose_name = 'Домик'
        verbose_name_plural = 'Домики'

    def __str__(self):
        return self.house_name



