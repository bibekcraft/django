# tourism/serializers.py
from rest_framework import serializers
from tourism.models import Category, Place, Details, Blog

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']

class PlaceSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Place
        fields = ['id', 'name', 'location', 'description', 'category', 'image', 'timetotravel']

class DetailsSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    place = serializers.PrimaryKeyRelatedField(queryset=Place.objects.all())

    class Meta:
        model = Details
        fields = [
            'id', 'name', 'location', 'difficulty', 'duration', 'tour_overview',
            'tour_highlights', 'whats_included', 'itinerary', 'recommendations',
            'must_try_food', 'recommended_guides', 'faqs', 'category', 'place',
            'image1', 'image2', 'image3', 'image4', 'image5', 'map_image'
        ]

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'image', 'createdAt', 'author']