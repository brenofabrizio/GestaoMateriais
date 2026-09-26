from decimal import Decimal

from rest_framework import serializers


class StockOperationSerializer(serializers.Serializer):
    material_id = serializers.IntegerField(min_value=1)
    warehouse_id = serializers.IntegerField(min_value=1)
    quantity = serializers.DecimalField(max_digits=14, decimal_places=3, min_value=Decimal('0.001'))
    idempotency_key = serializers.CharField(max_length=180)
    note = serializers.CharField(required=False, allow_blank=True)


class TransferSerializer(StockOperationSerializer):
    destination_warehouse_id = serializers.IntegerField(min_value=1)


class ReservationReleaseSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField(min_value=1)
    release_key = serializers.CharField(max_length=180)
    note = serializers.CharField(required=False, allow_blank=True)
