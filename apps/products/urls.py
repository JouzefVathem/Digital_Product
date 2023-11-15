from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    # ProductListView, ProductDetailView,
    # CategoryListView, CategoryDetailView,
    # FileListView, FileDetailView,
    ProductViewSet, ActiveProductList, CategoryViewSet, FileViewSet,
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'active-users-products', ActiveProductList, basename='active-users-products')
router.register(r'categories', CategoryViewSet)
router.register(r'files', FileViewSet)

urlpatterns = [
    # path('categories/', CategoryListView.as_view(), name='category-list'),  #
    # path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),  #
    #
    # path('products/', ProductListView.as_view(), name='product-list'),  #
    # path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),  #
    # path('products/active-users/', ActiveProductList.as_view({'get': 'list'}), name='active-users-products'),  #

    path('product/', include(router.urls)),

    # path('products/<int:product_id>/files/', FileListView.as_view(), name='file-list'),  #
    # path('products/<int:product_id>/files/<int:pk>/', FileDetailView.as_view(), name='file-detail'),  #
]
