from rest_framework import serializers, exceptions
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'interests', 'date_joined', 'photo')
        read_only_fields = ('date_joined',)


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})

        kwargs['style']['input_type'] = 'password'
        kwargs['write_only'] = True

        super().__init__(*args, **kwargs)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'interests', 'date_joined', 'photo', 'password')
        read_only_fields = ('date_joined',)

    def validate_username(self, username):
        if User.objects.filter(username__iexact=username).exists():
            raise exceptions.ValidationError('user with this username already exists.', code='unique')
        return username

    password = PasswordField(required=True)

    def create(self, validated_data):
        user = User(username=validated_data['username'], interests=validated_data.get('interests'), photo=validated_data.get('photo'))
        user.set_password(validated_data['password'])
        user.save()
        return user
