from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
import json
import re

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name')  # Update to use 'first_name'
            email = data.get('email')    # Required
            password = data.get('password')  # Required

            # Validation: Only first_name, email, and password are required
            if not all([first_name, email, password]):
                return JsonResponse({'error': 'First name, email, and password are required'}, status=400)
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
            if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
                return JsonResponse({'error': 'Password must be 8+ characters with letters and numbers'}, status=400)

            # Create user
            user = CustomUser.objects.create_user(username=email, email=email, password=password)
            user.first_name = first_name
            user.save()
            return JsonResponse({'message': 'Registration successful'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not all([email, password]):
                return JsonResponse({'error': 'Email and password are required'}, status=400)

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                response = JsonResponse({'message': 'Login successful'})
                response.set_cookie('logged_in', 'true', max_age=3600, httponly=True)
                return response
            return JsonResponse({'error': 'Invalid credentials or user not registered'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        response = JsonResponse({'message': 'Logout successful'})
        response.delete_cookie('logged_in')
        return response
    return JsonResponse({'error': 'Invalid request method'}, status=405)