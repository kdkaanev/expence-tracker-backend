from django.contrib import admin

from .models import Category, Transaction, Budget
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

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'spent', 'user')
    search_fields = ('category__name', 'user__username')
    list_filter = ('user',)
    ordering = ('category__name',)
# Register your models here.
