from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.inventory.models import StockReservation, Warehouse
from apps.inventory.serializers import (
    ReservationReleaseSerializer,
    StockOperationSerializer,
    TransferSerializer,
)
from apps.inventory.services import (
    issue_stock,
    receive_stock,
    release_stock,
    reserve_stock,
    transfer_stock,
)
from apps.materials.models import Material


def _material_and_warehouse(request, data):
    organization = request.user.organization
    material = get_object_or_404(Material, pk=data['material_id'], organization=organization)
    warehouse = get_object_or_404(Warehouse, pk=data['warehouse_id'], organization=organization)
    if material.organization_id != warehouse.organization_id:
        raise ValidationError('Material e almoxarifado devem pertencer à mesma organização.')
    return material, warehouse


def _movement_response(movement):
    return Response(
        {
            'id': movement.id,
            'kind': movement.kind,
            'quantity': f'{movement.quantity:.3f}',
            'balance_after': f'{movement.balance_after:.3f}',
            'warehouse_id': movement.warehouse_id,
            'material_id': movement.material_id,
            'idempotency_key': movement.idempotency_key,
        },
        status=status.HTTP_201_CREATED,
    )


class ReceiveStockView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = StockOperationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        material, warehouse = _material_and_warehouse(request, serializer.validated_data)
        try:
            movement = receive_stock(
                material=material, warehouse=warehouse,
                quantity=serializer.validated_data['quantity'],
                performed_by=request.user,
                idempotency_key=serializer.validated_data['idempotency_key'],
                note=serializer.validated_data.get('note', ''),
            )
        except ValidationError as exc:
            return Response({'detail': exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return _movement_response(movement)


class IssueStockView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = StockOperationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        material, warehouse = _material_and_warehouse(request, serializer.validated_data)
        try:
            movement = issue_stock(
                material=material, warehouse=warehouse,
                quantity=serializer.validated_data['quantity'],
                performed_by=request.user,
                idempotency_key=serializer.validated_data['idempotency_key'],
                note=serializer.validated_data.get('note', ''),
            )
        except ValidationError as exc:
            return Response({'detail': exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return _movement_response(movement)


class ReserveStockView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = StockOperationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        material, warehouse = _material_and_warehouse(request, serializer.validated_data)
        try:
            reservation = reserve_stock(
                material=material, warehouse=warehouse,
                quantity=serializer.validated_data['quantity'],
                reserved_by=request.user,
                reservation_key=serializer.validated_data['idempotency_key'],
                note=serializer.validated_data.get('note', ''),
            )
        except ValidationError as exc:
            return Response({'detail': exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'id': reservation.id, 'status': reservation.status, 'quantity': f'{reservation.quantity:.3f}'},
            status=status.HTTP_201_CREATED,
        )


class ReleaseStockView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ReservationReleaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reservation = get_object_or_404(
            StockReservation.objects.select_related('material', 'warehouse'),
            pk=serializer.validated_data['reservation_id'],
            material__organization=request.user.organization,
        )
        try:
            release_stock(
                reservation=reservation,
                released_by=request.user,
                release_key=serializer.validated_data['release_key'],
                note=serializer.validated_data.get('note', ''),
            )
        except ValidationError as exc:
            return Response({'detail': exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'id': reservation.id, 'status': reservation.status})


class TransferStockView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        material, source = _material_and_warehouse(request, serializer.validated_data)
        destination = get_object_or_404(
            Warehouse,
            pk=serializer.validated_data['destination_warehouse_id'],
            organization=request.user.organization,
        )
        try:
            movement = transfer_stock(
                material=material, source=source, destination=destination,
                quantity=serializer.validated_data['quantity'],
                performed_by=request.user,
                transfer_key=serializer.validated_data['idempotency_key'],
                note=serializer.validated_data.get('note', ''),
            )
        except ValidationError as exc:
            return Response({'detail': exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return _movement_response(movement)
