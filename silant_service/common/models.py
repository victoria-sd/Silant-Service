from django.db import models


class Dictionary(models.Model):
    """
    Общая модель для всех справочников.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"

    def __str__(self):
        return self.name


class DictionaryItem(models.Model):
    """
    Элемент справочника.
    """
    dictionary = models.ForeignKey(Dictionary, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочников"
        unique_together = ('dictionary', 'name')

    def __str__(self):
        return f"{self.dictionary.name}: {self.name}"

