from django.db import models
from django.contrib.auth import get_user_model
from common.models import DictionaryItem


User = get_user_model() # Используем кастомную модель User


class Machine(models.Model):
    """
    Ключевая сущность - "машина" (погрузчик).
    """
    # Справочники
    model_technique = models.ForeignKey(DictionaryItem, related_name='machines_model_technique',  verbose_name="Модель техники", on_delete=models.CASCADE, null=True, blank=True)
    model_engine = models.ForeignKey(DictionaryItem, related_name='machines_model_engine', verbose_name="Модель двигателя", on_delete=models.CASCADE, null=True, blank=True)
    model_transmission = models.ForeignKey(DictionaryItem, related_name='machines_model_transmission', verbose_name="Модель трансмиссии", on_delete=models.CASCADE, null=True, blank=True)
    model_drive_axle = models.ForeignKey(DictionaryItem, related_name='machines_model_drive_axle', verbose_name="Модель ведущего моста", on_delete=models.CASCADE, null=True, blank=True)
    model_steered_axle = models.ForeignKey(DictionaryItem, related_name='machines_model_steered_axle', verbose_name="Модель управляемого моста", on_delete=models.CASCADE, null=True, blank=True)

    # Текстовые поля (свободный ввод)
    serial_number_machine = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name="Зав. № машины")
    serial_number_engine = models.CharField(max_length=100, blank=True, null=True, verbose_name="Зав. № двигателя")
    serial_number_transmission = models.CharField(max_length=100, blank=True, null=True, verbose_name="Зав. № трансмиссии")
    serial_number_drive_axle = models.CharField(max_length=100, blank=True, null=True, verbose_name="Зав. № ведущего моста")
    serial_number_steered_axle = models.CharField(max_length=100, blank=True, null=True, verbose_name="Зав. № управляемого моста")
    delivery_contract = models.CharField(max_length=100, blank=True, null=True, verbose_name="Договор поставки №, дата")
    consignee = models.CharField(max_length=255, blank=True, null=True, verbose_name="Грузополучатель")
    delivery_address = models.TextField(blank=True, null=True, verbose_name="Адрес поставки (эксплуатации)")
    complexation = models.TextField(blank=True, null=True, verbose_name="Комплектация (доп. опции)")

    # Дата
    date_dispatch_from_factory = models.DateField(verbose_name="Дата отгрузки с завода")
    date_delivery_contract = models.DateField(blank=True, null=True, verbose_name="Дата договора поставки")

    # Связи с пользователями
    client = models.ForeignKey(User, related_name='machines_as_client', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Клиент")
    service_company = models.ForeignKey(User, related_name='machines_as_service_company', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сервисная компания")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"
        ordering = ['-date_dispatch_from_factory']

    def __str__(self):
        return f"({self.serial_number_machine})"
