from django.contrib import admin
from .models import Machine
from .forms import MachineForm


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    form = MachineForm
    list_display = (
        'serial_number_machine',
        'model_technique',
        'model_engine',
        'date_dispatch_from_factory',
        'client',
        'service_company'
    )
    list_filter = (
        'model_technique',
        'model_engine',
        'model_transmission',
        'model_drive_axle',
        'model_steered_axle',
        'client',
        'service_company'
    )
    search_fields = (
        'serial_number_machine',
        'serial_number_engine',
        'serial_number_transmission',
        'consignee',
        'delivery_address',
        'complexation',
        'client__username',
        'service_company__username',
    )
    readonly_fields = ('created_at', 'updated_at')