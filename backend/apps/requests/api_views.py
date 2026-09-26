from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.materials.models import Material
from apps.organizations.models import Area
from apps.requests.models import MaterialRequest, RequestItem
from apps.requests.serializers import (
    MaterialRequestCreateSerializer,
    MaterialRequestSerializer,
    RequestDecisionSerializer,
)
from apps.requests.services import approve_request, reject_request, submit_request


class RequestListCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = MaterialRequest.objects.filter(
            organization=request.user.organization,
        ).select_related('area', 'requester').prefetch_related('items__material')
        return Response(MaterialRequestSerializer(queryset, many=True).data)

    @transaction.atomic
    def post(self, request):
        serializer = MaterialRequestCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        area = get_object_or_404(Area, pk=data['area_id'], organization=request.user.organization)
        material_ids = [item['material_id'] for item in data['items']]
        materials = {
            material.id: material
            for material in Material.objects.filter(
                organization=request.user.organization,
                id__in=material_ids,
            )
        }
        if len(materials) != len(set(material_ids)):
            return Response(
                {'detail': 'Todos os materiais devem pertencer à organização do usuário.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        material_request = MaterialRequest.objects.create(
            organization=request.user.organization,
            requester=request.user,
            area=area,
            title=data['title'],
            justification=data.get('justification', ''),
        )
        RequestItem.objects.bulk_create([
            RequestItem(request=material_request, material=materials[item['material_id']], quantity=item['quantity'])
            for item in data['items']
        ])
        return Response(
            MaterialRequestSerializer(material_request).data,
            status=status.HTTP_201_CREATED,
        )


class RequestDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, request, pk):
        return get_object_or_404(
            MaterialRequest.objects.prefetch_related('items__material'),
            pk=pk,
            organization=request.user.organization,
        )

    def get(self, request, pk):
        return Response(MaterialRequestSerializer(self.get_object(request, pk)).data)


class RequestSubmitView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        material_request = get_object_or_404(MaterialRequest, pk=pk, organization=request.user.organization)
        try:
            material_request = submit_request(material_request, changed_by=request.user)
        except ValidationError as exc:
            return Response({'detail': exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MaterialRequestSerializer(material_request).data)


class RequestApproveView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        serializer = RequestDecisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        material_request = get_object_or_404(MaterialRequest, pk=pk, organization=request.user.organization)
        try:
            material_request = approve_request(
                material_request,
                approver=request.user,
                note=serializer.validated_data.get('note', ''),
            )
        except ValidationError as exc:
            return Response({'detail': exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MaterialRequestSerializer(material_request).data)


class RequestRejectView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        serializer = RequestDecisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        material_request = get_object_or_404(MaterialRequest, pk=pk, organization=request.user.organization)
        try:
            material_request = reject_request(
                material_request,
                approver=request.user,
                note=serializer.validated_data.get('note', ''),
            )
        except ValidationError as exc:
            return Response({'detail': exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MaterialRequestSerializer(material_request).data)
