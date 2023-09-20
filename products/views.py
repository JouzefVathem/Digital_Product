from rest_framework import views, response, status, viewsets, permissions

from .models import Category, Product, File
from .serializers import CategorySerializer, ProductSerializer, FileSerializer

# class ProductListView (viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryListView(views.APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return response.Response(data=serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailView(views.APIView):

    def get_object(self, pk):
        try :
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        return category

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, context={'request': request})
        return response.Response(data=serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ProductListView(views.APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return response.Response(data=serializer.data)
    
    def post (self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(views.APIView):

    def get_object(self, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        return product

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, context={'request': request})
        return response.Response(data=serializer.data)
    
    def put (self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

class FileListView(views.APIView):

    def get(self, request, product_id):
        files = File.objects.filter(product_id=product_id)
        serializer = FileSerializer(files, many=True, context={'request': request})
        return response.Response(data=serializer.data)
    
    def post(self, request, product_id):
        serializer = FileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(product_id=product_id)
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileDetailView(views.APIView):

    def get_object(self, pk):
        try:
            file = File.objects.get(pk=pk)
        except File.DoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        return file

    def get(self, request, product_id , pk):
        file = self.get_object(pk)
        serializer = FileSerializer(file, context={'request': request})
        return response.Response(data=serializer.data)
    
    def put(self, request, product_id , pk):
        file = self.get_object(product_id, pk)
        serializer = FileSerializer(file, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, product_id , pk):
        file = self.get_object(product_id, pk)
        file.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)