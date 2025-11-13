from django import forms
from .models import Machine
from common.models import DictionaryItem


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Фильтруем "Модель техники"
        if 'model_technique' in self.fields:
            self.fields['model_technique'].queryset = DictionaryItem.objects.filter(
                dictionary__name='Модель техники' # Указываем имя справочника
            )

        # Фильтруем "Модель двигателя"
        if 'model_engine' in self.fields:
            self.fields['model_engine'].queryset = DictionaryItem.objects.filter(
                dictionary__name='Модель двигателя'
            )

        if 'model_transmission' in self.fields:
            self.fields['model_transmission'].queryset = DictionaryItem.objects.filter(
                dictionary__name='Модель трансмиссии'
            )

        if 'model_drive_axle' in self.fields:
            self.fields['model_drive_axle'].queryset = DictionaryItem.objects.filter(
                dictionary__name='Модель ведущего моста'
            )

        if 'model_steered_axle' in self.fields:
            self.fields['model_steered_axle'].queryset = DictionaryItem.objects.filter(
                dictionary__name='Модель управляемого моста'
            )
