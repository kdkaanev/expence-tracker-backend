from django.utils.dateparse import parse_date
from rest_framework import viewsets, permissions
from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user).select_related('category')
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        date_str = self.request.query_params.get('date')
        if date_str:
            parsed_date = parse_date(date_str)
            if parsed_date:
                queryset = queryset.filter(created_at__date=parsed_date)

        start_data = self.request.query_params.get('start')
        end_data = self.request.query_params.get('end')
        if start_data and end_data:
            start_date = parse_date(start_data)
            end_date = parse_date(end_data)
            if start_date and end_date:
                queryset = queryset.filter(created_at__date__range=(start_date, end_date))
        return queryset

