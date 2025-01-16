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
        print('self.validated_data:', self.validated_data)
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
            UserProfile.objects.create(user=account, username=username, type=type, email=email)
            return account


class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = '__all__'
