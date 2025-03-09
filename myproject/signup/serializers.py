from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()  # This will use the CustomUser model
        fields = ['first_name', 'email', 'password']  # Correct field name
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['email'],  # Use email as username
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name']  # Correct field name
        )   
        return user
