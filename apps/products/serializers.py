from rest_framework import serializers

from apps.users.models import User
from .models import Category, Product, File


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='title', allow_null=True,
                                          required=False)

    class Meta:
        model = Category
        fields = ('id', 'parent', 'title', 'description', 'avatar', 'url', 'is_enable')

    def create(self, validated_data):
        parent = validated_data.pop('parent')
        category = Category.objects.create(**validated_data)
        category.parent = parent
        category.save()
        return category

    def update(self, instance, validated_data):
        instance.parent = validated_data.get('parent', instance.parent)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.is_enable = validated_data.get('is_enable', instance.is_enable)
        instance.save()
        return instance


class FileSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field='title')
    file_type = serializers.SerializerMethodField(method_name='get_file_type')

    class Meta:
        model = File
        fields = ('id', 'title', 'product', 'file', 'file_type', 'url', 'is_enable')

    @staticmethod
    def get_file_type(obj):
        return obj.get_file_type_display()

    def create(self, validated_data):
        product = validated_data.pop('product')
        file_type = validated_data.pop('file_type')
        file = File.objects.create(**validated_data, file_type=file_type)
        file.product = product
        file.save()
        return file

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.product = validated_data.get('product', instance.product)
        instance.file = validated_data.get('file', instance.file)
        instance.file_type = validated_data.get('file_type', instance.file_type)
        instance.is_enable = validated_data.get('is_enable', instance.is_enable)
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    # categories = CategorySerializer(many=True)
    categories = serializers.HyperlinkedRelatedField(many=True, queryset=Category.objects.all(),
                                                     view_name='category-detail')
    # files = FileSerializer(many=True)
    files = serializers.HyperlinkedRelatedField(many=True, queryset=File.objects.all(), view_name='file-detail')

    class Meta:
        model = Product
        fields = ('id', 'title', 'user', 'description', 'avatar', 'categories', 'files', 'url', 'is_enable')

    def create(self, validated_data):
        user = validated_data.pop('user')
        categories = validated_data.pop('categories')
        files = validated_data.pop('files')
        product = Product.objects.create(**validated_data)
        product.user = user
        product.categories = categories
        product.files = files
        product.save()
        return product

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.categories = validated_data.get('categories', instance.categories)
        instance.files = validated_data.get('files', instance.files)
        instance.is_enable = validated_data.get('is_enable', instance.is_enable)
        instance.save()
        return instance
