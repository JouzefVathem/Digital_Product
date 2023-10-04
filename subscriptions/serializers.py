from rest_framework import serializers

from .models import Package, Subscription


class PackageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id ', 'title', 'sku', 'description', 'avatar', 'price', 'duration')


class SubscriptionSerializers(serializers.ModelSerializer):
    package = PackageSerializers()

    class Meta:
        model = Subscription
        fields = ('package', 'created_time', 'expire_time')
