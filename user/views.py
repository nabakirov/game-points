from rest_framework import generics, exceptions, response, viewsets, mixins
from . import serializers, models
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


def get_login_response(user, request):
    refresh = RefreshToken.for_user(user)
    data = {
        "user": serializers.UserSerializer(instance=user, context={'request': request}).data,
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }
    return data


class LoginView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(True)
        user = authenticate(**serializer.validated_data)
        if not user:
            raise exceptions.AuthenticationFailed()
        # todo: update last_login in background
        user.last_login = timezone.now()
        user.save()
        return response.Response(data=get_login_response(user, request))


class UsersView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return models.User.objects.all()


class SignUpView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(True)
        serializer.save()
        return response.Response(data=get_login_response(serializer.instance, request))


class ProfileView(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = serializers.UserSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_object(self):
        return self.request.user
