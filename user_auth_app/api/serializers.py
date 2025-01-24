from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=['customer', 'business'], write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
    
    def save(self):
        """
        Checks whether the passwords match and whether the email address already exists.
        If it's valid a new User object and UserProfile object will be created.
        Return value is the User object.
        """
        username = self.validated_data['username']
        email = self.validated_data['email']
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        type = self.validated_data['type']

        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'Passwords don\'t match'})
        
        try:
            existing_user = User.objects.get(email=email)
        except:
            existing_user = None
        
        if existing_user:
            print('existing User with that email: ', existing_user)
            raise serializers.ValidationError({'error': 'Email already exists!'})
        else:
            account = User(username=username, email=email)
            account.set_password(pw)
            account.save()
            UserProfile.objects.create(id=account.id, user=account, username=username, type=type, email=email)
            return account


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']

    def update(self, instance, validated_data):
        """
        Function for updating specific fields for the UserProfile object and User object.
        """
        for field in self.Meta.fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        
        for field in ['username', 'first_name', 'last_name', 'email']:
            if field in validated_data:
                setattr(instance.user, field, validated_data[field])

        instance.user.save()
        instance.save()
        return instance
    
    def to_representation(self, instance):
        """
        Function for the representation for the current instance.
        """
        representation = super().to_representation(instance)
        if instance.file:
            representation['file'] = instance.file.url
        return representation


class BusinessUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type']

    def to_representation(self, instance):
        """
        Function for the representation for the current instance.
        """
        representation = super().to_representation(instance)
        response_data = {}

        response_data['user'] = {
            'pk': representation.get('user'),
            'username': representation.get('username'),
            'first_name': representation.get('first_name'),
            'last_name': representation.get('last_name')
        }
        response_data['file'] = representation.get('file')
        response_data['location'] = representation.get('location')
        response_data['tel'] = representation.get('tel')
        response_data['description'] = representation.get('description')
        response_data['working_hours'] = representation.get('working_hours')
        response_data['type'] = representation.get('type')
        return response_data


class CustomerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'type', 'created_at']

    def to_representation(self, instance):
        """
        Function for the representation for the current instance.
        """
        representation = super().to_representation(instance)
        response_data = {}

        response_data['user'] = {
            'pk': representation.get('user'),
            'username': representation.get('username'),
            'first_name': representation.get('first_name'),
            'last_name': representation.get('last_name')
        }
        response_data['file'] = representation.get('file')
        response_data['created_at'] = representation.get('created_at')
        response_data['type'] = representation.get('type')
        return response_data
