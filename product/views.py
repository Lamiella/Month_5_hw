from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from .models import Product, Category, Review
from .serializers import (
    CategoryListSerializer, CategoryDetailSerializer,
    ProductListSerializer, ProductDetailSerializer,
    ReviewListSerializer, ReviewDetailSerializer
)


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = ProductListSerializer(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category = request.data.get('category')

        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category=category
        )
        product.save()

    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductDetailSerializer(product, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category_id')
        product.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def categories_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.annotate(products_count=Count('product'))
        data = CategoryListSerializer(categories, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        name = request.data.get('name')

        category = Category.objects.create(name=name)
        category.save()
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategoryDetailSerializer(category, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        category.name = request.data.get('name')
        category.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerializer(category).data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewListSerializer(reviews, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        stars = request.data.get('stars')
        text = request.data.get('text')
        product = request.data.get('product')

        review = Review.objects.create(
            stars=stars,
            text=text,
            product=product
        )
        review.save()


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewDetailSerializer(review, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        review.stars = request.data.get('stars')
        review.text = request.data.get('text')
        review.product_id = request.data.get('product_id')
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewDetailSerializer(review).data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)