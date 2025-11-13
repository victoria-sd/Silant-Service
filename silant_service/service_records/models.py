from django.db import models
from machines.models import Machine
from common.models import DictionaryItem
from django.db.models import F
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


class Maintenance(models.Model):
    """
    Сущность "ТО" (техническое обслуживание).
    """
    # Связи
    type_of_maintenance = models.ForeignKey(DictionaryItem, related_name='maintenance_type', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Вид ТО")
    organization_performing_maintenance = models.ForeignKey(DictionaryItem, related_name='maintenance_performing_org', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Организация, проводившая ТО")
    machine = models.ForeignKey(Machine, related_name='maintenance_records', on_delete=models.CASCADE, verbose_name="Машина")
    service_company = models.ForeignKey(User, related_name='maintenance_by_service_company', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сервисная компания")

    # Числовое и текстовое поля
    mileage_hours = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Наработка, м/час")
    work_order_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="№ заказ-наряда")

    # Дата
    date_of_maintenance = models.DateField(verbose_name="Дата проведения ТО")
    date_work_order = models.DateField(blank=True, null=True, verbose_name="Дата заказ-наряда")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Техническое обслуживание"
        verbose_name_plural = "Технические обслуживания"
        ordering = ['-date_of_maintenance']

    def __str__(self):
        return f"{self.machine} - {self.type_of_maintenance} ({self.date_of_maintenance})"


class Reclamation(models.Model):
    """
    Сущность "Рекламации".
    """
    # Связи
    failure_node = models.ForeignKey(DictionaryItem, related_name='reclamations_failure_node', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Узел отказа")
    restoration_method = models.ForeignKey(DictionaryItem, related_name='reclamations_restoration_method', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Способ восстановления")
    machine = models.ForeignKey(Machine, related_name='reclamation_records', on_delete=models.CASCADE, verbose_name="Машина")
    service_company = models.ForeignKey(User, related_name='reclamations_by_service_company', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сервисная компания")

    # Числовое и текстовое поля
    mileage_hours = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Наработка, м/час")
    downtime_hours = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Время простоя техники, дни", editable=False) # Расчетное поле
    description_of_failure = models.TextField(verbose_name="Описание отказа")
    spare_parts_used = models.TextField(blank=True, null=True, verbose_name="Используемые запасные части")

    # Дата
    date_of_failure = models.DateTimeField(verbose_name="Дата отказа")
    date_of_restoration = models.DateTimeField(blank=True, null=True, verbose_name="Дата восстановления")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Рекламация"
        verbose_name_plural = "Рекламации"
        ordering = ['-date_of_failure']

    def save(self, *args, **kwargs):
        if self.date_of_failure and self.date_of_restoration:
            # Расчет времени простоя
            time_difference = self.date_of_restoration - self.date_of_failure
            self.downtime_hours = time_difference.total_seconds() / 86400 #Расчет в днях
        else:
            self.downtime_hours = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.machine} - {self.failure_node} ({self.date_of_failure})"

