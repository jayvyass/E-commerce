from rest_framework import serializers
from .models import Products , BillingDetail, Category1 ,Category2


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingDetail
        fields = ['user','subtotal','discount','total','products','first_name','last_name','town_city','country','address','postcode_zip','mobile','email','order_notes']

class ProductSerializer(serializers.ModelSerializer):
    # These fields are used for output (GET requests)
    category1 = serializers.CharField(source='category1.name', read_only=True)
    category2 = serializers.CharField(source='category2.name', read_only=True)

    # These fields are used for input (POST/PUT requests)
    category1_name = serializers.CharField(write_only=True, required=False)
    category2_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Products
        fields = [
            'product_id', 'name', 'image', 'description', 'price', 'weight', 'country', 'out_of_stock',
            'category1', 'category2',  # Output fields for GET
            'category1_name', 'category2_name'  # Input fields for POST/PUT
        ]

    def validate(self, data):
        # Handle category1_name_input to find the related category1
        category1_name = data.pop('category1_name', None)
        if category1_name:
            try:
                category1 = Category1.objects.get(name=category1_name)
                data['category1'] = category1
            except Category1.DoesNotExist:
                raise serializers.ValidationError({"category1_name": "Category1 with this name does not exist."})

        # Handle category2_name_input to find the related category2
        category2_name = data.pop('category2_name', None)
        if category2_name:
            try:
                category2 = Category2.objects.get(name=category2_name)
                data['category2'] = category2
            except Category2.DoesNotExist:
                raise serializers.ValidationError({"category2_name": "Category2 with this name does not exist."})

        return data

    def create(self, validated_data):
        # Use the validated data to create a new product instance
        product = Products.objects.create(
            name=validated_data.get('name'),
            image=validated_data.get('image'),
            description=validated_data.get('description'),
            price=validated_data.get('price'),
            weight=validated_data.get('weight'),
            country=validated_data.get('country'),
            out_of_stock=validated_data.get('out_of_stock'),
            category1=validated_data.get('category1'),
            category2=validated_data.get('category2')
        )
        return product

    def update(self, instance, validated_data):
        # Update the instance with the validated data
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.country = validated_data.get('country', instance.country)
        instance.out_of_stock = validated_data.get('out_of_stock', instance.out_of_stock)
        instance.category1 = validated_data.get('category1', instance.category1)
        instance.category2 = validated_data.get('category2', instance.category2)

        instance.save()
        return instance








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

    



        

