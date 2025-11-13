from django.shortcuts import render
from django.views import View
from .models import Machine
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.db.models import Q
from common.models import DictionaryItem


# --- Для не авторизованных пользователей ---
class MachineSearchView(View):
    def get(self, request):
        serial_number = request.GET.get('serial_number')
        if not serial_number:
            return render(request, 'machines/public_search.html', {'error': 'Введите заводской номер.'})

        try:
            machine = Machine.objects.get(serial_number_machine=serial_number)
            # Возвращаем только часть полей, доступных гостю
            data = {
                'Зав. № машины': machine.serial_number_machine,
                'Модель техники': machine.model_technique.name if machine.model_technique else None,
                'Модель двигателя': machine.model_engine.name if machine.model_engine else None,
                'Зав. № двигателя': machine.serial_number_engine if machine.serial_number_engine else None,
                'Модель трансмиссии (производитель, артикул)': machine.model_transmission.name if machine.model_transmission else None,
                'Зав. № трансмиссии': machine.serial_number_transmission if machine.serial_number_transmission else None,
                'Модель ведущего моста': machine.model_drive_axle.name if machine.model_drive_axle else None,
                'Зав. № ведущего моста': machine.serial_number_drive_axle if machine.serial_number_drive_axle else None,
                'Модель управляемого моста': machine.model_steered_axle.name if machine.model_steered_axle else None,
                'Зав. № управляемого моста': machine.serial_number_steered_axle if machine.serial_number_steered_axle else None,
            }
            return render(request, 'machines/public_search.html', {'machine_data': data})
        except Machine.DoesNotExist:
            return render(request, 'machines/public_search.html', {'error': 'Машина с таким заводским номером не найдена.'})
        except Exception as e:
            return render(request, 'machines/public_search.html', {'error': f'Произошла ошибка: {e}'})


class BaseMachineListView(LoginRequiredMixin, ListView):
    model = Machine
    template_name = 'machines/machine_list.html'
    context_object_name = 'machines'

    def get_queryset(self):
        user = self.request.user
        # Базовая фильтрация по пользователю
        if user.is_staff:  # Менеджер
            queryset = Machine.objects.all()
        elif user.groups.filter(name='Клиент').exists(): # Клиент
            queryset = Machine.objects.filter(client=user)
        elif user.groups.filter(name='Сервисная организация').exists(): # Сервисная организация
            queryset = Machine.objects.filter(service_company=user)
        else:
            queryset = Machine.objects.none()

        query = Q()
        request_get = self.request.GET

        # Фильтры для моделей
        # Модель техники
        if request_get.get('model_technique'):
            model_technique_id = int(request_get['model_technique'])
            query &= Q(model_technique_id=model_technique_id)

        # Модель двигателя
        if request_get.get('model_engine'):
            model_engine_id = int(request_get['model_engine'])
            query &= Q(model_engine_id=model_engine_id)

        # Модель трансмиссии
        if request_get.get('model_transmission'):
            model_transmission_id = int(request_get['model_transmission'])
            query &= Q(model_transmission_id=model_transmission_id)

        # Модель управляемого моста
        if request_get.get('model_steered_axle'):
            model_steered_axle_id = int(request_get['model_steered_axle'])
            query &= Q(model_steered_axle_id=model_steered_axle_id)

        # Модель ведущего моста
        if request_get.get('model_drive_axle'):
            model_drive_axle_id = int(request_get['model_drive_axle'])
            query &= Q(model_drive_axle_id=model_drive_axle_id)

        queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.get_role()
        context['models_technique'] = DictionaryItem.objects.filter(dictionary__name='Модель техники').order_by('name')
        context['models_engine'] = DictionaryItem.objects.filter(dictionary__name='Модель двигателя').order_by('name')
        context['models_transmission'] = DictionaryItem.objects.filter(dictionary__name='Модель трансмиссии').order_by('name')
        context['models_steered_axle'] = DictionaryItem.objects.filter(dictionary__name='Модель управляемого моста').order_by('name')
        context['models_drive_axle'] = DictionaryItem.objects.filter(dictionary__name='Модель ведущего моста').order_by('name')
        context['filter_params'] = self.request.GET
        return context


class MachineListView(BaseMachineListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-date_dispatch_from_factory')


class MachineDetailView(LoginRequiredMixin, DetailView):
    model = Machine
    template_name = 'machines/machine_detail.html'
    context_object_name = 'machine'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Machine.objects.all()
        elif user.groups.filter(name='Клиент').exists():
            return Machine.objects.filter(client=user, pk=self.kwargs['pk'])
        elif user.groups.filter(name='Сервисная организация').exists():
            return Machine.objects.filter(service_company=user, pk=self.kwargs['pk'])
        else:
            return Machine.objects.none()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        machine = self.object
        context['maintenance_records'] = machine.maintenance_records.all().order_by('date_of_maintenance')
        context['reclamation_records'] = machine.reclamation_records.all().order_by('date_of_failure')
        context['user_role'] = self.request.user.get_role()
        return context

