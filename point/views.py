from rest_framework import mixins, viewsets
from . import models, serializers
from gamepoints.mixins import ActionSerializerClassMixin


class TransactionViewSet(ActionSerializerClassMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    action_serializer_class = {
        "retrieve": serializers.TransactionDetailSerializer,
        "create": serializers.TransactionCreationSerializer
    }
    serializer_class = serializers.TransactionSerializer

    def get_queryset(self):
        return models.Transaction.objects.all()
