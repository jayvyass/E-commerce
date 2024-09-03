from rest_framework import serializers
from .models import Products , BillingDetail, Category1 ,Category2


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingDetail
        fields = ['user','subtotal','discount','total','products','first_name','last_name','town_city','country','address','postcode_zip','mobile','email','order_notes']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'







# class Category1Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category1
#         fields = ['id', 'name']

# class Category2Serializer(serializers.ModelSerializer):
#     parent_category = Category1Serializer()

#     class Meta:
#         model = Category2
#         fields = ['id', 'name', 'parent_category']

# class ProductSerializer(serializers.ModelSerializer):
#     category1 = Category1Serializer()
#     category2 = Category2Serializer()
#     image = serializers.ImageField(required=False) 

#     class Meta:
#         model = Products
#         fields = '__all__'

#     def create(self, validated_data):
#         # Extract category data
#         category1_data = validated_data.pop('category1', None)
#         category2_data = validated_data.pop('category2', None)

#         # Initialize category1
#         category1 = None
#         if category1_data:
#             category1_id = category1_data.get('id')
#             if category1_id:
#                 category1 = Category1.objects.filter(id=category1_id).first()
#             if not category1:
#                 category1, created = Category1.objects.get_or_create(**category1_data)

#         # Initialize category2 and parent_category
#         category2 = None
#         parent_category = None
#         if category2_data:
#             parent_category_data = category2_data.pop('parent_category', None)
#             if parent_category_data:
#                 parent_category_id = parent_category_data.get('id')
#                 if parent_category_id:
#                     parent_category = Category1.objects.filter(id=parent_category_id).first()
#                 if not parent_category:
#                     parent_category, created = Category1.objects.get_or_create(**parent_category_data)

#             category2_id = category2_data.get('id')
#             if category2_id:
#                 category2 = Category2.objects.filter(id=category2_id).first()
#             if not category2:
#                 category2, created = Category2.objects.get_or_create(parent_category=parent_category, **category2_data)

#         # Ensure the product is unique based on specific fields
#         product_data = {
#             'name': validated_data.get('name'),
#             'price': validated_data.get('price'),
#             'category1': category1,
#             'category2': category2,
#         }

#         existing_product = Products.objects.filter(
#             name=product_data['name'],
#             price=product_data['price'],
#             category1=product_data['category1'],
#             category2=product_data['category2']
#         ).first()

#         if existing_product:
#             return existing_product

#         # Create a new product if no existing product found
#         product = Products.objects.create(category1=category1, category2=category2, **validated_data)
#         return product

    



        

