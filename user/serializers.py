from rest_framework import serializers, exceptions
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'interests', 'date_joined', 'photo', 'points')
        read_only_fields = ('date_joined', 'points')

    def validate_username(self, username):
        if User.objects.filter(username__iexact=username).exists():
            raise exceptions.ValidationError('user with this username already exists.', code='unique')
        return username


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
        fields = ('id', 'username', 'interests', 'date_joined', 'photo', 'password', 'points')
        read_only_fields = ('date_joined', 'points')

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


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = PasswordField(required=True)
    new_password = PasswordField(required=True)

    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise exceptions.ValidationError('incorrect password')
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance