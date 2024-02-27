from rest_framework import serializers
import requests
from .models import CloudProvider, Digitalocean, Linode, AWS

class ProviderUserSerializerBase(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CloudProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = CloudProvider
        fields = '__all__'


class DigitaloceanSerializer(ProviderUserSerializerBase):
    class Meta:
        model = Digitalocean
        fields = '__all__'

    def validate_api_key(self, value):
        if not self.valid_do_api_key(value):
            raise serializers.ValidationError("This is not a valid API key format for Digitalocean.")
        return value

    def valid_do_api_key(self, api_key):
        headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
        url = "https://api.digitalocean.com/v2/account"
        response = requests.get(url, headers=headers)
        return response.status_code == requests.codes.ok


class LinodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Linode
        fields = '__all__'

class AWSSerializer(serializers.ModelSerializer):
    class Meta:
        model = AWS
        fields = '__all__'
