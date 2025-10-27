from django.utils.dateparse import parse_date
from rest_framework import viewsets, permissions, status
from .models import Category, Transaction, Budget, Pots 
from .serializers import CategorySerializer, TransactionSerializer, BudgetSerializer, PotsSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction as db_transaction
from decimal import Decimal
from django.utils.timezone import now
from decimal import Decimal, ROUND_HALF_UP

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
    
class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user).select_related('category')

class PotsViewSet(viewsets.ModelViewSet):
    queryset = Pots.objects.all()
    serializer_class = PotsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Pots.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=True, methods=['post'])
    @db_transaction.atomic
    def add_funds(self, request, pk=None):
        pot = self.get_object()
        amount = Decimal(str(request.data.get('amount', 0))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if amount <= 0:
            return Response({'error': 'Amount must be positive.'}, status=status.HTTP_400_BAD_REQUEST)
        with db_transaction.atomic():
            pot.saved = (pot.saved + amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            pot.save()

            category, _ = Category.objects.get_or_create(name='Pots', owner=self.request.user)

            Transaction.objects.create(
                amount=amount,
                category=category,
                description=f'Added funds to pot {pot.pot}',
                type='expense',
                transaction_date=now(),
                user=self.request.user,
                pot=pot
            )
        return Response(PotsSerializer(pot).data, status=status.HTTP_200_OK)
    
    
    @action(detail=True, methods=['post'])
    @db_transaction.atomic
    def withdraw_funds(self, request, pk=None):
        pot = self.get_object()
        amount = Decimal(str(request.data.get('amount', 0))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if amount <= 0:
            return Response({'error': 'Amount must be positive.'}, status=status.HTTP_400_BAD_REQUEST)
        if amount > pot.saved:
            return Response({'error': 'Insufficient funds in the pot.'}, status=status.HTTP_400_BAD_REQUEST)

        pot.saved = (pot.saved - amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        pot.save()
        category, _ = Category.objects.get_or_create(name='Pots', owner=self.request.user)
            
        Transaction.objects.create(
                amount=amount,
                category=category,
                description=f'Withdrew funds from pot {pot.pot}',
                type='income',
                transaction_date=now(),
                user=self.request.user,
                pot=pot
            )
        return Response(PotsSerializer(pot).data, status=status.HTTP_200_OK)