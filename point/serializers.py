from rest_framework import serializers as s, exceptions
from . import models, settings
from user.serializers import UserSerializer


class TransactionSerializer(s.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = ('id', 'user', 'type', 'value', 'date', 'description')
        read_only_fields = ('date',)


class TransactionCreationSerializer(s.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = ('id', 'type', 'value', 'date', 'description')
        read_only_fields = ('date',)

    def validate_value(self, value):
        if value <= 0:
            raise exceptions.ValidationError('value must be positive')
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        if attrs['type'] == settings.TransactionType.exchange:
            if user.points < attrs['value']:
                raise exceptions.ValidationError('not enough point to exchange')
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        if validated_data['type'] == settings.TransactionType.add:
            user.points += validated_data['value']
        elif validated_data['type'] == settings.TransactionType.exchange:
            user.points -= validated_data['value']
        user.save()
        validated_data['user'] = user
        return super().create(validated_data)


class TransactionDetailSerializer(s.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = ('id', 'user', 'type', 'value', 'date', 'description')
        read_only_fields = ('date',)
    user = UserSerializer()
