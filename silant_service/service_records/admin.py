from django.contrib import admin
from .models import Maintenance, Reclamation
from .forms import MaintenanceForm, ReclamationForm


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    form = MaintenanceForm
    list_display = (
        'machine',
        'type_of_maintenance',
        'date_of_maintenance',
        'mileage_hours',
        'work_order_number',
        'organization_performing_maintenance',
        'service_company'
    )
    list_filter = (
        'type_of_maintenance',
        'organization_performing_maintenance',
        'service_company',
        ('date_of_maintenance', admin.DateFieldListFilter),
    )
    search_fields = (
        'machine__serial_number_machine',
        'work_order_number',
        'service_company__username',
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Reclamation)
class ReclamationAdmin(admin.ModelAdmin):
    form = ReclamationForm
    list_display = (
        'machine',
        'date_of_failure',
        'failure_node',
        'description_of_failure',
        'date_of_restoration',
        'downtime_hours',
        'service_company'
    )
    list_filter = (
        'failure_node',
        'restoration_method',
        'service_company',
        ('date_of_failure', admin.DateFieldListFilter),
        ('date_of_restoration', admin.DateFieldListFilter),
    )
    search_fields = (
        'machine__serial_number_machine',
        'description_of_failure',
        'spare_parts_used',
        'service_company__username',
    )
    readonly_fields = ('downtime_hours', 'created_at', 'updated_at')