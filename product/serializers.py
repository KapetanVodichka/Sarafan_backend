from rest_framework import serializers

from product.models import SubCategory, Category, Product, CartItem


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'slug', 'image')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image', 'subcategories')


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    subcategory_name = serializers.CharField(source='subcategory.name')
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        return [image.url for image in [obj.image1, obj.image2, obj.image3] if image]

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'category_name', 'subcategory_name', 'price', 'images')


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']