from .models import User, Organisation
from rest_framework import serializers
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    This serializer converts User model instances to and from JSON format.
    It ensures that the password field is write-only, meaning it will not be
    included in the serialized representation when reading user data, but it
    will be included when creating or updating user data.

    Attributes:
        Meta (class): Inner class that defines the metadata for the serializer.
    """
    class Meta:
        model = User
        fields = ['userId', 'firstName', 'lastName', 'email', 'password', 'phone']
        extra_kwargs = {
			'password': {'write_only': True}
		}
        
    def create(self, validated_data):
        password = validated_data.get('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        
        return instance
    
    
class OrganisationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Organisation model.

    This serializer converts Organisation model instances to and from JSON format.
    It uses Django REST Framework's ModelSerializer to automatically generate fields 
    based on the Organisation model.

    Attributes:
        Meta (class): Inner class that defines the metadata for the serializer.
    """
    class Meta:
        model = Organisation
        fields = ['orgId', 'name', 'description']