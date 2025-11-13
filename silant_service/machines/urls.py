from django.urls import path
from . import views
from service_records.views import MaintenanceListViewForMachine, ReclamationListViewForMachine, MaintenanceCreateView, ReclamationCreateView


urlpatterns = [
    path('public/search/', views.MachineSearchView.as_view(), name='machine_public_search'),  # URL для гостя: поиск по заводскому номеру
    path('list/', views.MachineListView.as_view(), name='machine_list'),
    path('<int:pk>/', views.MachineDetailView.as_view(), name='machine_detail'),
    path('<int:machine_pk>/maintenance/', MaintenanceListViewForMachine.as_view(), name='maintenance_list_for_machine'),
    path('<int:machine_pk>/reclamations/', ReclamationListViewForMachine.as_view(), name='reclamation_list_for_machine'),
    path('<int:machine_pk>/maintenance/add', MaintenanceCreateView.as_view(), name='maintenance_create'),
    path('<int:machine_pk>/reclamations/add/', ReclamationCreateView.as_view(), name='reclamation_create'),
]