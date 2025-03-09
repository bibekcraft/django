# tourism/views.py
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from signup.serializers import UserRegistrationSerializer
from .models import Category, Place, Details, Blog
from .serializers import CategorySerializer, PlaceSerializer, DetailsSerializer, BlogSerializer
import logging

logger = logging.getLogger(__name__)

# Authentication Views
@api_view(['POST'])
def register_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, username=email, password=password)
    if user:
        login(request, user)
        response = Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
        response.set_cookie('logged_in', 'true', max_age=3600, httponly=True)
        return response
    return Response({"message": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    response = Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)
    response.delete_cookie('logged_in')
    return response

# Category CRUD
@api_view(['GET'])
def get_all_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_category_by_id(request, id):
    try:
        category = Category.objects.get(pk=id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        logger.error(f"Invalid ID format: {id}")
        return Response({'error': 'Invalid category ID'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def add_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# tourism/views.py (partial)
@api_view(['PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def update_category(request, id):
    try:
        category = Category.objects.get(id=id)
        if request.method == 'PUT':
            serializer = CategorySerializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            if Place.objects.filter(category_id=id).exists() or Details.objects.filter(category_id=id).exists():
                return Response(
                    {'error': 'Cannot delete category with associated places or details'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            category.delete()
            return Response({"message": "Category deleted successfully"}, status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        logger.error(f"Category not found for id: {id}")
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        logger.error(f"Invalid ID format received: {id}")
        return Response({'error': 'Invalid category ID'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error processing request for id {id}: {str(e)}")
        return Response({'error': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
def delete_category(request, id):
    try:
        category = Category.objects.get(pk=id)
        if Place.objects.filter(category_id=id).exists() or Details.objects.filter(category_id=id).exists():
            return Response(
                {'error': 'Cannot delete category with associated places or details'},
                status=status.HTTP_400_BAD_REQUEST
            )
        category.delete()
        return Response({"message": "Category deleted successfully"}, status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        logger.error(f"Category not found for id: {id}")
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        logger.error(f"Invalid ID format: {id}")
        return Response({'error': 'Invalid category ID'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_places_by_category(request, id):
    try:
        places = Place.objects.filter(category_id=id)
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)
    except ValueError:
        logger.error(f"Invalid ID format: {id}")
        return Response({'error': 'Invalid category ID'}, status=status.HTTP_400_BAD_REQUEST)

# Place CRUD
@api_view(['GET'])
def get_all_places(request):
    category_id = request.query_params.get('category')
    if category_id:
        try:
            places = Place.objects.filter(category_id=category_id)
        except ValueError:
            return Response({'error': 'Invalid category ID'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        places = Place.objects.all()
    serializer = PlaceSerializer(places, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_place_by_id(request, id):
    try:
        place = Place.objects.get(pk=id)
        serializer = PlaceSerializer(place)
        return Response(serializer.data)
    except Place.DoesNotExist:
        return Response({'error': 'Place not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def add_place(request):
    serializer = PlaceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@parser_classes([MultiPartParser, FormParser])
def update_place(request, id):
    try:
        place = Place.objects.get(pk=id)
        serializer = PlaceSerializer(place, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Place.DoesNotExist:
        return Response({'error': 'Place not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@parser_classes([MultiPartParser, FormParser])
def delete_place(request, id):
    try:
        place = Place.objects.get(pk=id)
        place.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Place.DoesNotExist:
        return Response({'error': 'Place not found'}, status=status.HTTP_404_NOT_FOUND)

# Details CRUD
@api_view(['GET'])
def get_all_details(request):
    details = Details.objects.all()
    serializer = DetailsSerializer(details, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_detail_by_id(request, id):
    try:
        detail = Details.objects.get(pk=id)
        serializer = DetailsSerializer(detail)
        return Response(serializer.data)
    except Details.DoesNotExist:
        return Response({'error': 'Detail not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])  # Changed to handle file uploads
def add_detail(request):
    serializer = DetailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@parser_classes([MultiPartParser, FormParser])
def update_detail(request, id):
    try:
        detail = Details.objects.get(pk=id)
        serializer = DetailsSerializer(detail, data=request.data, partial=True)  # Partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Details.DoesNotExist:
        return Response({'error': 'Detail not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_detail(request, id):
    try:
        detail = Details.objects.get(pk=id)
        detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Details.DoesNotExist:
        return Response({'error': 'Detail not found'}, status=status.HTTP_404_NOT_FOUND)

# Blog CRUD
@api_view(['GET'])
def get_all_blogs(request):
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_blog_by_id(request, id):
    try:
        blog = Blog.objects.get(pk=id)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    except Blog.DoesNotExist:
        return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def add_blog(request):
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@parser_classes([MultiPartParser, FormParser])
def update_blog(request, id):
    try:
        blog = Blog.objects.get(id=id)
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Blog.DoesNotExist:
        return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_blog(request, id):
    try:
        blog = Blog.objects.get(pk=id)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Blog.DoesNotExist:
        return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

# Chatbot
@api_view(['POST'])
def chatbot(request):
    message = request.data.get("message", "").strip()
    if not message:
        return Response({"reply": "Please say something!"}, status=status.HTTP_400_BAD_REQUEST)
    if "hello" in message.lower():
        reply = "Hi there! How can I help you today?"
    elif "latest post" in message.lower():
        latest_blog = Blog.objects.order_by('-createdAt').first()  # Fixed to use createdAt
        reply = f"The latest post is '{latest_blog.title}' from {latest_blog.createdAt.strftime('%Y-%m-%d')}." if latest_blog else "No posts yet!"
    else:
        reply = f"I'm not sure how to respond to '{message}'. Try asking about blogs or saying hello!"
    return Response({"reply": reply}, status=status.HTTP_200_OK)
@api_view(['GET'])
def get_all_places(request):
    category_id = request.query_params.get('category')
    if category_id:
        try:
            places = Place.objects.filter(category_id=category_id)
        except ValueError:
            return Response({'error': 'Invalid category ID'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        places = Place.objects.all()
    serializer = PlaceSerializer(places, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def get_places_by_category(request, id):
    try:
        places = Place.objects.filter(category_id=id)
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)
    except ValueError:
        logger.error(f"Invalid ID format: {id}")
        return Response({'error': 'Invalid category ID'}, status=status.HTTP_400_BAD_REQUEST)