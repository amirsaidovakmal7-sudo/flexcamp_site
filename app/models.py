from django.db import models



class House(models.Model):
    house_name = models.CharField(max_length=128, verbose_name='Название домика')
    house_description = models.TextField('Описание для домика')
    house_price = models.DecimalField(max_digits=25, decimal_places=2, verbose_name='Стоимость аренды в суммах')
    class Meta:
        verbose_name = 'Домик'
        verbose_name_plural = 'Домики'

    def __str__(self):
        return self.house_name



class House_photo(models.Model):
    house_name = models.TextField('Название домика', default='Домик')
    house_photo = models.ImageField(upload_to='media', verbose_name='Фотография домика')
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотки'
    def __str__(self):
        return self.house_name
