from django.db import models

# Create your models here.


class Currency(models.Model):
    code = models.TextField()
    name = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name + '-' + self.code


class CurrencyPerDate(models.Model):
    currency = models.ForeignKey(
        Currency,
        related_name='value',
        on_delete=models.CASCADE,
    )
    value = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )
    nominal = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )
    date = models.DateField()

    class Meta:
        ordering = ['-date']

