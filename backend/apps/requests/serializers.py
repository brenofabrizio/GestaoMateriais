from decimal import Decimal

from rest_framework import serializers

from apps.requests.models import MaterialRequest, RequestItem


class RequestItemInputSerializer(serializers.Serializer):
    material_id = serializers.IntegerField(min_value=1)
    quantity = serializers.DecimalField(max_digits=14, decimal_places=3, min_value=Decimal('0.001'))


class MaterialRequestCreateSerializer(serializers.Serializer):
    area_id = serializers.IntegerField(min_value=1)
    title = serializers.CharField(max_length=180)
    justification = serializers.CharField(required=False, allow_blank=True)
    items = RequestItemInputSerializer(many=True, allow_empty=False)


class RequestDecisionSerializer(serializers.Serializer):
    note = serializers.CharField(required=False, allow_blank=True)


class MaterialRequestSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = MaterialRequest
        fields = ('id', 'code', 'title', 'justification', 'status', 'area_id', 'requester_id', 'items', 'created_at')

    def get_items(self, obj):
        return [
            {
                'id': item.id,
                'material_id': item.material_id,
                'sku': item.material.sku,
                'name': item.material.name,
                'quantity': f'{item.quantity:.3f}',
                'approved_quantity': f'{item.approved_quantity:.3f}',
            }
            for item in obj.items.select_related('material').all()
        ]
