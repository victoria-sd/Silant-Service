from django import forms
from .models import Maintenance, Reclamation
from common.models import DictionaryItem
from machines.models import Machine
from django.contrib.auth import get_user_model
User = get_user_model()


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['machine', 'type_of_maintenance', 'date_of_maintenance', 'mileage_hours', 'work_order_number',
                  'date_work_order', 'organization_performing_maintenance']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'type_of_maintenance' in self.fields:
            self.fields['type_of_maintenance'].queryset = DictionaryItem.objects.filter(
                dictionary__name='Вид ТО'
            )
        if 'organization_performing_maintenance' in self.fields:
            self.fields['organization_performing_maintenance'].queryset = DictionaryItem.objects.filter(
                dictionary__name='Организация, проводившая ТО'
            )


class ReclamationForm(forms.ModelForm):
    class Meta:
        model = Reclamation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'failure_node' in self.fields:
            self.fields['failure_node'].queryset = DictionaryItem.objects.filter(
                dictionary__name='Узел отказа'
            )
        if 'restoration_method' in self.fields:
            self.fields['restoration_method'].queryset = DictionaryItem.objects.filter(
                dictionary__name='Способ восстановления'
            )
        if 'service_company' in self.fields:
            self.fields['service_company'].queryset = User.objects.filter(
                groups='2'
            )


class MaintenanceCreateForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['machine', 'type_of_maintenance', 'date_of_maintenance', 'mileage_hours', 'work_order_number', 'date_work_order', 'organization_performing_maintenance']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.machine_pk = kwargs.pop('machine_pk', None)
        self.types_of_maintenance_queryset = kwargs.pop('types_of_maintenance_queryset', None)
        self.organization_performing_maintenance_queryset = kwargs.pop('organization_performing_maintenance_queryset', None)

        super().__init__(*args, **kwargs)

        if self.user:
            machine_instance = Machine.objects.get(pk=self.machine_pk)
            self.fields['machine'].initial = machine_instance
            self.fields['machine'].disabled = True

            self.fields['type_of_maintenance'].queryset = self.types_of_maintenance_queryset
            self.fields['organization_performing_maintenance'].queryset = self.organization_performing_maintenance_queryset


class ReclamationCreateForm(forms.ModelForm):
    class Meta:
        model = Reclamation
        fields = ['machine', 'date_of_failure', 'mileage_hours', 'failure_node', 'description_of_failure', 'restoration_method', 'spare_parts_used', 'date_of_restoration', 'service_company'] # Укажите все нужные поля

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.machine_pk = kwargs.pop('machine_pk', None)
        self.failure_nodes_queryset = kwargs.pop('failure_nodes_queryset', None)
        self.restoration_methods_queryset = kwargs.pop('restoration_methods_queryset', None)

        super().__init__(*args, **kwargs)

        if self.user and self.user.is_authenticated:
            if self.user.groups.filter(name='Сервисная организация').exists():
                # Для сервисной организации, сервисную компанию заполняем автоматически
                self.fields['service_company'].disabled = True
                self.fields['service_company'].initial = self.user

            machine_instance = Machine.objects.get(pk=self.machine_pk)
            self.fields['machine'].initial = machine_instance
            self.fields['machine'].disabled = True

            self.fields['failure_node'].queryset = self.failure_nodes_queryset
            self.fields['restoration_method'].queryset = self.restoration_methods_queryset