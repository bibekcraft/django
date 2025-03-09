# tourism/urls.py
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from tourism import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('api/signup/register/', views.register_view, name='register'),
    path('api/signup/login/', views.login_view, name='login'),
    path('api/signup/logout/', views.logout_view, name='logout'),

    # Chatbot
    path('chatbot/', views.chatbot, name='chatbot'),

    # Details CRUD
    path('api/details/all/', views.get_all_details, name='get_all_details'),
    path('api/details/<int:id>/', views.get_detail_by_id, name='get_detail_by_id'),
    path('api/details/add/', views.add_detail, name='add_detail'),
    path('api/details/update/<int:id>/', views.update_detail, name='update_detail'),
    path('api/details/delete/<int:id>/', views.delete_detail, name='delete_detail'),

    # Place CRUD
    path('api/places/all/', views.get_all_places, name='get_all_places'),
    path('api/places/<int:id>/', views.get_place_by_id, name='get_place_by_id'),
    path('api/places/add/', views.add_place, name='add_place'),
    path('api/places/update/<int:id>/', views.update_place, name='update_place'),
    path('api/places/delete/<int:id>/', views.delete_place, name='delete_place'),
    path('api/places/', views.get_all_places, name='get_all_places'),  # Changed from 'all/'
    path('api/places/<int:id>/', views.get_place_by_id, name='get_place_by_id'),

    # Category CRUD
    path('api/categories/<int:id>/places/', views.get_places_by_category, name='get_places_by_category'),
    path('api/categories/all/', views.get_all_categories, name='get_all_categories'),
    path('api/categories/<int:id>/', views.get_category_by_id, name='get_category_by_id'),
    path('api/categories/add/', views.add_category, name='add_category'),
    path('api/categories/update/<int:id>/', views.update_category, name='update_category'),
    path('api/categories/delete/<int:id>/', views.delete_category, name='delete_category'),

    # Blog CRUD
    path('api/blog/all/', views.get_all_blogs, name='get_all_blogs'),
    path('api/blog/add/', views.add_blog, name='add_blog'),
    path('api/blog/<int:id>/', views.get_blog_by_id, name='get_blog_by_id'),
    path('api/blog/update/<int:id>/', views.update_blog, name='update_blog'),
    path('api/blog/delete/<int:id>/', views.delete_blog, name='delete_blog'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)