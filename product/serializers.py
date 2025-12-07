from rest_framework import serializers
from .models import Product, Category, Review
from rest_framework.exceptions import ValidationError


class CategoryListSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ['name', 'products_count']


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    product = serializers.CharField()
    rating = serializers.FloatField(source='product.rating')

    class Meta:
        model = Review
        fields = ['product', 'text', 'stars', 'rating']


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    reviews = ReviewListSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews']


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=1, max_length=255)
    description = serializers.CharField(required=False)
    price = serializers.FloatField()
    category = serializers.ListField(child=serializers.IntegerField())

    def validate_category(self, category):
        category = list(set(category))
        category_from_db = Category.objects.filter(id__in=category)
        if len(category) != len(category_from_db):
            raise ValidationError('Category do not exist!')
        return category


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=1, max_length=255)


class ReviewValidateSerializer(serializers.Serializer):
    stars = serializers.IntegerField(min_value=1, max_value=10)
    text = serializers.CharField(required=False)
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product does not exist!')
        return product_id