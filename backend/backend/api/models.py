from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

CATEGORY_CHOICES = [
    ("expense", "Expense"),
    ("income", "Income"),
]


class Category(models.Model):
    name = models.CharField(max_length=100)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return self.name


class Transaction(models.Model):
    description = models.TextField(blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    type = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default=False)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="cat_transactions"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_transactions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_date = models.DateField()

    def __str__(self):
        return f"{self.amount} in {self.category.name}"


class Budget(models.Model):

    amount = models.DecimalField(decimal_places=2, max_digits=10)
    spent = models.DecimalField(
        decimal_places=2, max_digits=10, default=0
    )  # New field to track spent amount

    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_budgets"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="cat_budgets"
    )


class Meta:
    unique_together = ("user", "category", "start_date", "end_date")


def __str__(self):
    return f"{self.user} - {self.category.name}: {self.amount} лв."
