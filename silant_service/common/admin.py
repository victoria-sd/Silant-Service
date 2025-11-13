from django.contrib import admin
from .models import Dictionary, DictionaryItem

@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(DictionaryItem)
class DictionaryItemAdmin(admin.ModelAdmin):
    list_display = ('dictionary', 'name', 'description')
    list_filter = ('dictionary',)
    search_fields = ('name', 'description')
