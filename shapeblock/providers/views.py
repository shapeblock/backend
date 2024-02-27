import logging

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import CloudProvider
from .serializers import CloudProviderSerializer, DigitaloceanSerializer, LinodeSerializer, AWSSerializer
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger("django")

class ProviderViewSet(viewsets.GenericViewSet):
    """
    A viewset that provides `create`, `retrieve`, and `delete` actions for all provider types.
    """
    queryset = CloudProvider.objects.all()
    serializer_class = CloudProviderSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if 'cloud' in self.request.data:
            cloud = self.request.data['cloud']
            if cloud == 'digitalocean':
                return DigitaloceanSerializer
            elif cloud == 'linode':
                return LinodeSerializer
            elif cloud == 'aws':
                return AWSSerializer
        return CloudProviderSerializer

    def get_queryset(self):
        return CloudProvider.objects.all()

    def perform_create(self, serializer):
      serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
          serializer.save(user=self.request.user)
          return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CloudProviderSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        provider = queryset.get(uuid=pk)
        serializer = CloudProviderSerializer(provider)
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        provider = self.get_queryset().get(uuid=pk)
        provider.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
