from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Order
from .permissions import IsBuyerOrReadOnly
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsBuyerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_buyer:
            return Order.objects.filter(buyer=user).select_related("buyer").prefetch_related("items__product")
        elif user.is_farmer:
            return Order.objects.filter(items__product__farmer=user).distinct().select_related("buyer").prefetch_related("items__product")
        return Order.objects.none()

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)