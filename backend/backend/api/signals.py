from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Transaction, Budget
from django.db.models import Sum, F

# Signal to update the budget when a transaction is created or deleted

def recalculate_budget_spent(category):
    budget = Budget.objects.filter(category=category).first()
    if not budget:
        return
    total_spent = Transaction.objects.filter(category=category, type='expense').aggregate(total=Sum(F('amount')))['total']
    budget.spent = total_spent if total_spent else 0
    budget.save(update_fields=['spent'])
       

@receiver(post_save, sender=Transaction)
def  update_budget_spent_on_save(sender, instance, created, **kwargs):
    recalculate_budget_spent(instance.category)

# Signal to update the budget when a transaction is deleted

@receiver(post_delete, sender=Transaction)
def update_budget_spent_on_delete(sender, instance, **kwargs):
    recalculate_budget_spent(instance.category)