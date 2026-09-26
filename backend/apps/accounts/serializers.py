from rest_framework import serializers

from apps.accounts.models import User


class OrganizationSummarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.CharField()


class AreaSummarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    code = serializers.CharField()
    name = serializers.CharField()


class CurrentUserSerializer(serializers.ModelSerializer):
    organization = OrganizationSummarySerializer(read_only=True)
    area = AreaSummarySerializer(read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'organization', 'area', 'is_active',
        )

    def get_full_name(self, obj):
        return obj.get_full_name().strip() or obj.email
