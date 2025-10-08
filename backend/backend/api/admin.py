from django.contrib import admin

from .models import Category, Transaction
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner',)
    search_fields = ('name', 'owner__username')
    list_filter = ('owner',)
    ordering = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'category', 'user', 'transaction_date', 'created_at')
    search_fields = ('category__name', 'user__username', 'description')
    list_filter = ('category', 'user', 'transaction_date')
    ordering = ('-created_at',)
# Register your models here.
