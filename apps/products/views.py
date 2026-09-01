from rest_framework import viewsets

from .models import Category, Product
from .permissions import IsFarmerOwnerOrReadOnly
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Browse-only — categories are managed via /admin/, not this API."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []  # public


class ProductViewSet(viewsets.ModelViewSet):
    """
    /api/products/products/         GET (list, filterable), POST (farmer creates)
    /api/products/products/{id}/    GET, PUT/PATCH (owner only), DELETE (owner only)

    Query params supported on list: ?county=Nyeri&category=vegetables&search=tomato
    """
    serializer_class = ProductSerializer
    permission_classes = [IsFarmerOwnerOrReadOnly]

    def get_queryset(self):
        qs = Product.objects.select_related("farmer", "category")
        if self.action == "list":
            qs = qs.filter(is_active=True)

        county = self.request.query_params.get("county")
        category = self.request.query_params.get("category")
        search = self.request.query_params.get("search")

        if county:
            qs = qs.filter(county__iexact=county)
        if category:
            qs = qs.filter(category__slug=category)
        if search:
            qs = qs.filter(name__icontains=search)

        return qs

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)