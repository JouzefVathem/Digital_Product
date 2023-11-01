from rest_framework import serializers

from apps.users.models import User
from .models import Category, Product, File


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='title')

    class Meta:
        model = Category
        fields = ('id', 'parent', 'title', 'description', 'avatar', 'url')


class FileSerializer(serializers.ModelSerializer):
    file_type = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('id', 'title', 'file', 'file_type')

    @staticmethod
    def get_file_type(obj):
        return obj.get_file_type_display()


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    categories = CategorySerializer(many=True)
    # files = FileSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'user',  'description', 'avatar', 'categories', 'url')
