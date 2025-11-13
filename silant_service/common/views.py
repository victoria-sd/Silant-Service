from django.shortcuts import render
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import DictionaryItem


class DictionaryItemDetailView(DetailView):
    model = DictionaryItem
    template_name = 'common/dictionary_item_detail.html'
    context_object_name = 'item'

    def get_object(self, queryset=None):
        return get_object_or_404(DictionaryItem, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Описание: {context['item'].name}"

        return context