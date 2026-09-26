from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.inventory.models import StockBalance, Warehouse
from apps.inventory.services import receive_stock
from apps.materials.models import Material, MaterialCategory
from apps.organizations.models import Organization


class InventoryApiTests(APITestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name='Empresa API')
        category = MaterialCategory.objects.create(
            organization=self.organization,
            code='ADM',
            name='Administrativo',
        )
        self.material = Material.objects.create(
            organization=self.organization,
            category=category,
            sku='ADM-PAPEL-001',
            name='Papel A4',
        )
        self.warehouse = Warehouse.objects.create(
            organization=self.organization,
            code='ALM-ADM',
            name='Almoxarifado Administrativo',
        )
        self.user = User.objects.create_user(
            email='estoque@empresa-api.com',
            password='Strong-password-123',
            organization=self.organization,
        )
        receive_stock(
            material=self.material,
            warehouse=self.warehouse,
            quantity=Decimal('10'),
            performed_by=self.user,
            idempotency_key='api-receipt-001',
        )
        response = self.client.post(
            reverse('auth-token'),
            {'email': self.user.email, 'password': 'Strong-password-123'},
            format='json',
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_issue_endpoint_changes_balance(self):
        response = self.client.post(
            reverse('inventory-issue'),
            {
                'material_id': self.material.id,
                'warehouse_id': self.warehouse.id,
                'quantity': '3',
                'idempotency_key': 'api-issue-001',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['balance_after'], '7.000')
        self.assertEqual(StockBalance.objects.get().qty_on_hand, Decimal('7'))

    def test_inventory_operation_requires_authentication(self):
        self.client.credentials()

        response = self.client.post(reverse('inventory-issue'), {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
