from django.shortcuts import render
from service_records.models import Maintenance, Reclamation
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView
from django.db.models import Q
from machines.models import Machine
from django.shortcuts import get_object_or_404
from common.models import DictionaryItem
from django.contrib.auth import get_user_model
from .forms import MaintenanceCreateForm, ReclamationCreateForm
from django.urls import reverse_lazy


User = get_user_model()


class MaintenanceListViewForMachine(LoginRequiredMixin, ListView):
    model = Maintenance
    template_name = 'service_records/maintenance_list_for_machine.html'
    context_object_name = 'maintenance_list'

    def get_queryset(self):
        self.machine = get_object_or_404(Machine, pk=self.kwargs['machine_pk'])
        queryset = Maintenance.objects.filter(machine=self.machine)
        query = Q()
        request_get = self.request.GET

        # Фильтры для таблицы "TO"
        # вид ТО
        if request_get.get('type_of_maintenance'):
            type_of_maintenance_id = int(request_get['type_of_maintenance'])
            query &= Q(type_of_maintenance=type_of_maintenance_id)

        # Сервисная компания
        if request_get.get('service_company'):
            service_company_id = int(request_get['service_company'])
            query &= Q(service_company_id=service_company_id, service_company__groups__name='Сервисная организация')

        queryset = queryset.filter(query).order_by('-date_of_maintenance')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = self.machine
        context['filter_params'] = self.request.GET
        context['types_of_maintenance'] = DictionaryItem.objects.filter(dictionary__name='Вид ТО').order_by('name')
        context['service_companies'] = User.objects.filter(groups='2').order_by('username')
        return context


class ReclamationListViewForMachine(LoginRequiredMixin, ListView):
    model = Reclamation
    template_name = 'service_records/reclamation_list_for_machine.html'
    context_object_name = 'reclamation_list'

    def get_queryset(self):
        self.machine = get_object_or_404(Machine, pk=self.kwargs['machine_pk'])
        queryset = Reclamation.objects.filter(machine=self.machine)
        query = Q()
        request_get = self.request.GET

        # Фильтры для таблицы "Рекламация"
        # Узел отказа
        if request_get.get('failure_node'):
            failure_node_id = int(request_get['failure_node'])
            query &= Q(failure_node_id=failure_node_id)

        # Способ восстановления
        if request_get.get('restoration_method'):
            restoration_method_id = int(request_get['restoration_method'])
            query &= Q(restoration_method_id=restoration_method_id)

        # Сервисная компания
        if request_get.get('service_company'):
            service_company_id = int(request_get['service_company'])
            query &= Q(service_company_id=service_company_id)

        queryset = queryset.filter(query).order_by('-date_of_failure')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = self.machine
        context['filter_params'] = self.request.GET
        context['failure_nodes'] = DictionaryItem.objects.filter(dictionary__name='Узел отказа').order_by('name')
        context['restoration_methods'] = DictionaryItem.objects.filter(dictionary__name='Способ восстановления').order_by('name')
        context['service_companies'] = User.objects.filter(groups='2').order_by('username')
        return context


class MaintenanceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Maintenance
    form_class = MaintenanceCreateForm
    template_name = 'service_records/maintenance_create.html'

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Клиент', 'Сервисная организация']).exists() or self.request.user.is_superuser

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        machine_pk = self.kwargs.get('machine_pk')
        if machine_pk:
            kwargs['machine_pk'] = machine_pk
            # Фильтруем для вида ТО
        if DictionaryItem.objects.filter(dictionary__name='Вид ТО').exists():
            kwargs['types_of_maintenance_queryset'] = DictionaryItem.objects.filter(dictionary__name='Вид ТО').order_by('name')
        else:
            kwargs['types_of_maintenance_queryset'] = DictionaryItem.objects.none()
            # Фильтруем для организации, проводившей ТО
        if DictionaryItem.objects.filter(dictionary__name='Организация, проводившая ТО').exists():
            kwargs['organization_performing_maintenance_queryset'] = DictionaryItem.objects.filter(
                dictionary__name='Организация, проводившая ТО').order_by('name')
        else:
            kwargs['organization_performing_maintenance_queryset'] = DictionaryItem.objects.none()
        return kwargs

    def form_valid(self, form):
        maintenance = form.save(commit=False)
        user = self.request.user
        if user.groups.filter(name='Клиент').exists():
            maintenance.client = user
        elif user.groups.filter(name='Сервисная организация').exists():
            maintenance.service_company = user

        machine = Machine.objects.get(pk=self.kwargs['machine_pk'])
        maintenance.machine = machine
        maintenance.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить ТО'
        machine_pk = self.kwargs.get('machine_pk')
        if machine_pk:
            context['machine_pk'] = machine_pk
        return context

    def get_success_url(self):
        machine_pk = self.kwargs.get('machine_pk')
        if machine_pk:
            return reverse_lazy('maintenance_list_for_machine', kwargs={'machine_pk': machine_pk})
        else:
            return reverse_lazy('machine_list')


class ReclamationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Reclamation
    form_class = ReclamationCreateForm
    template_name = 'service_records/reclamation_create.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Сервисная организация').exists() or self.request.user.is_superuser

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        machine_pk = self.kwargs.get('machine_pk')
        if machine_pk:
            kwargs['machine_pk'] = machine_pk
            # Фильтруем для узла отказа
        if DictionaryItem.objects.filter(dictionary__name='Узел отказа').exists():
            kwargs['failure_nodes_queryset'] = DictionaryItem.objects.filter(dictionary__name='Узел отказа').order_by('name')
        else:
            kwargs['failure_nodes_queryset'] = DictionaryItem.objects.none()
            # Фильтруем для способа восстановления
        if DictionaryItem.objects.filter(dictionary__name='Способ восстановления').exists():
            kwargs['restoration_methods_queryset'] = DictionaryItem.objects.filter(dictionary__name='Способ восстановления').order_by('name')
        else:
            kwargs['restoration_methods_queryset'] = DictionaryItem.objects.none()
        return kwargs

    def form_valid(self, form):
        reclamation = form.save(commit=False)
        user = self.request.user
        reclamation.service_company = user
        machine = Machine.objects.get(pk=self.kwargs['machine_pk'])
        reclamation.machine = machine
        reclamation.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить рекламацию'
        machine_pk = self.kwargs.get('machine_pk')
        if machine_pk:
            context['machine_pk'] = machine_pk
        return context

    def get_success_url(self):
        machine_pk = self.kwargs.get('machine_pk')
        if machine_pk:
            return reverse_lazy('reclamation_list_for_machine', kwargs={'machine_pk': machine_pk})
        else:
            return reverse_lazy('machine_list')