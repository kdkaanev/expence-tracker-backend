from rest_framework import serializers
from .models import Category, Transaction, Budget


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name","owner"]
        read_only_fields = ["owner"]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()


    class Meta:
        model = Transaction
        fields = ["id", "amount", "category_name", "user","description","transaction_date","category", 'type']
        read_only_fields = ["user","created_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def get_category_name(self, obj):
        return obj.category.name.lower() if obj.category else None
    
    
    
class BudgetSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Budget
        fields = ["id", "amount", "spent", "category", "category_name", "transactions", "user", "created_at"]
        read_only_fields = ["user", "created_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def get_category_name(self, obj):
        return obj.category.name.lower() if obj.category else None
