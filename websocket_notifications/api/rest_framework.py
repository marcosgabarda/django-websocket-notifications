from rest_framework import serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from websocket_notifications.models import NotificationGroup


class NotificationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationGroup
        fields = ["code"]


class NotificationGroupViewSet(viewsets.ModelViewSet):
    queryset = NotificationGroup.objects.all()
    serializer_class = NotificationGroupSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        instance = self.queryset.model.objects.filter(user=self.request.user).first()
        if not instance:
            instance, _ = self.queryset.model.objects.get_or_create_for_user(
                user=self.request.user
            )
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
