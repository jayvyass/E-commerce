from rest_framework import serializers
from .models import Products , BillingDetail, Category1 ,Category2


class Category1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Category1
        fields = ['id', 'name']  # Adjust based on your Category1 model fields

class Category2Serializer(serializers.ModelSerializer):
    full_category_name = serializers.SerializerMethodField()

    class Meta:
        model = Category2
        fields = ['id', 'name', 'full_category_name']

    def get_full_category_name(self, obj):
        # Assuming Category2 has a ForeignKey to Category1 called parent_category
        if obj.parent_category:
            return f"{obj.parent_category.name} > {obj.name}"
        return obj.name
    
class ProductSerializer(serializers.ModelSerializer):
    category1 = Category1Serializer()
    category2 = Category2Serializer()

    class Meta:
        model = Products
        fields = ['product_id', 'name', 'image', 'description', 'price', 'weight', 'country', 'out_of_stock', 'created_at', 'category1', 'category2']

class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingDetail
        fields = '__all__'