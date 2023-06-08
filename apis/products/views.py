from products.models import Product
from django.shortcuts import get_object_or_404
from apis.products.serializers import ProductsSerializer
from rest_framework import viewsets
from rest_framework.response import Response


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductsSerializer
    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = ProductsSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = ProductsSerializer(product)
        return Response(serializer.data)
