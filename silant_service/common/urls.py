from django.urls import path
from . import views

urlpatterns = [
    path('dictionary/item/<int:pk>/', views.DictionaryItemDetailView.as_view(), name='dictionary_item_detail'),
]