from rest_framework import serializers
from .models import Category, Transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "owner"]
        read_only_fields = ["owner"]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M")

    class Meta:
        model = Transaction
        fields = ["id", "amount", "category_name", "user", "created_at","description"]
        read_only_fields = ["user",]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def get_category_name(self, obj):
        return obj.category.name.lower() if obj.category else None
