from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.materials.models import Material, MaterialCategory
from apps.organizations.models import Area, Organization
from apps.requests.models import MaterialRequest


class RequestApiTests(APITestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name='Empresa API')
        self.area = Area.objects.create(organization=self.organization, code='TI', name='Tecnologia')
        category = MaterialCategory.objects.create(organization=self.organization, code='TI', name='Tecnologia')
        self.material = Material.objects.create(
            organization=self.organization,
            category=category,
            sku='TI-TECLADO-001',
            name='Teclado',
        )
        self.requester = User.objects.create_user(
            email='solicitante-api@exemplo.com',
            password='Strong-password-123',
            organization=self.organization,
            area=self.area,
        )
        self.approver = User.objects.create_user(
            email='gestor-api@exemplo.com',
            password='Strong-password-123',
            organization=self.organization,
            area=self.area,
        )
        login = self.client.post(
            reverse('auth-token'),
            {'email': self.requester.email, 'password': 'Strong-password-123'},
            format='json',
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")

    def test_user_can_create_and_submit_request(self):
        create = self.client.post(
            reverse('request-list-create'),
            {
                'area_id': self.area.id,
                'title': 'Teclado novo',
                'justification': 'Equipamento danificado',
                'items': [{'material_id': self.material.id, 'quantity': '2'}],
            },
            format='json',
        )
        self.assertEqual(create.status_code, status.HTTP_201_CREATED)
        request_id = create.data['id']

        submit = self.client.post(reverse('request-submit', args=[request_id]), {}, format='json')

        self.assertEqual(submit.status_code, status.HTTP_200_OK)
        self.assertEqual(submit.data['status'], MaterialRequest.Status.PENDING_APPROVAL)
        self.assertEqual(submit.data['items'][0]['quantity'], '2.000')

    def test_request_can_be_approved_by_another_user(self):
        create = self.client.post(
            reverse('request-list-create'),
            {
                'area_id': self.area.id,
                'title': 'Monitor',
                'items': [{'material_id': self.material.id, 'quantity': '1'}],
            },
            format='json',
        )
        request_id = create.data['id']
        self.client.post(reverse('request-submit', args=[request_id]), {}, format='json')

        login = self.client.post(
            reverse('auth-token'),
            {'email': self.approver.email, 'password': 'Strong-password-123'},
            format='json',
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        approve = self.client.post(
            reverse('request-approve', args=[request_id]),
            {'note': 'Aprovado'},
            format='json',
        )

        self.assertEqual(approve.status_code, status.HTTP_200_OK)
        self.assertEqual(approve.data['status'], MaterialRequest.Status.APPROVED)
        self.assertEqual(approve.data['items'][0]['approved_quantity'], '1.000')
