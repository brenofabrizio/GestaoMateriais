from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.accounts.models import User
from apps.inventory.models import StockBalance, StockMovement, StockReservation, Warehouse
from apps.inventory.services import (
    issue_stock,
    receive_stock,
    release_stock,
    reserve_stock,
    transfer_stock,
)
from apps.materials.models import Material, MaterialCategory
from apps.organizations.models import Organization


class InventoryServiceTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name='Empresa Exemplo')
        category = MaterialCategory.objects.create(
            organization=self.organization,
            code='TI',
            name='Tecnologia',
        )
        self.material = Material.objects.create(
            organization=self.organization,
            category=category,
            sku='TI-MOUSE-001',
            name='Mouse sem fio',
        )
        self.warehouse = Warehouse.objects.create(
            organization=self.organization,
            code='ALM-TI',
            name='Almoxarifado de TI',
        )
        self.user = User.objects.create_user(
            email='estoque@exemplo.com',
            password='Strong-password-123',
            organization=self.organization,
        )

    def test_receive_creates_balance_and_immutable_movement(self):
        movement = receive_stock(
            material=self.material,
            warehouse=self.warehouse,
            quantity=Decimal('10'),
            performed_by=self.user,
            idempotency_key='receipt-001',
        )

        balance = StockBalance.objects.get(material=self.material, warehouse=self.warehouse)
        self.assertEqual(balance.qty_on_hand, Decimal('10'))
        self.assertEqual(movement.balance_after, Decimal('10'))
        self.assertEqual(StockMovement.objects.count(), 1)

    def test_issue_rejects_quantity_above_available_balance(self):
        receive_stock(
            material=self.material,
            warehouse=self.warehouse,
            quantity=Decimal('5'),
            performed_by=self.user,
            idempotency_key='receipt-002',
        )

        with self.assertRaises(ValidationError):
            issue_stock(
                material=self.material,
                warehouse=self.warehouse,
                quantity=Decimal('6'),
                performed_by=self.user,
                idempotency_key='issue-001',
            )

        self.assertEqual(StockMovement.objects.count(), 1)

    def test_issue_reduces_balance(self):
        receive_stock(
            material=self.material,
            warehouse=self.warehouse,
            quantity=Decimal('10'),
            performed_by=self.user,
            idempotency_key='receipt-003',
        )
        movement = issue_stock(
            material=self.material,
            warehouse=self.warehouse,
            quantity=Decimal('3'),
            performed_by=self.user,
            idempotency_key='issue-002',
        )

        balance = StockBalance.objects.get(material=self.material, warehouse=self.warehouse)
        self.assertEqual(balance.qty_on_hand, Decimal('7'))
        self.assertEqual(movement.balance_after, Decimal('7'))

    def test_same_idempotency_key_does_not_duplicate_movement(self):
        first = receive_stock(
            material=self.material,
            warehouse=self.warehouse,
            quantity=Decimal('10'),
            performed_by=self.user,
            idempotency_key='receipt-unique',
        )
        second = receive_stock(
            material=self.material,
            warehouse=self.warehouse,
            quantity=Decimal('10'),
            performed_by=self.user,
            idempotency_key='receipt-unique',
        )

        self.assertEqual(first.pk, second.pk)
        self.assertEqual(StockMovement.objects.count(), 1)
        self.assertEqual(StockBalance.objects.get().qty_on_hand, Decimal('10'))

    def test_reservation_reduces_available_without_reducing_physical_stock(self):
        receive_stock(
            material=self.material,
            warehouse=self.warehouse,
            quantity=Decimal('10'),
            performed_by=self.user,
            idempotency_key='receipt-reservation',
        )

        reservation = reserve_stock(
            material=self.material,
            warehouse=self.warehouse,
            quantity=Decimal('4'),
            reserved_by=self.user,
            reservation_key='reservation-001',
        )

        balance = StockBalance.objects.get()
        self.assertEqual(reservation.status, StockReservation.Status.ACTIVE)
        self.assertEqual(balance.qty_on_hand, Decimal('10'))
        self.assertEqual(balance.qty_reserved, Decimal('4'))
        self.assertEqual(balance.qty_available, Decimal('6'))

    def test_release_returns_reserved_quantity_to_available(self):
        receive_stock(
            material=self.material,
            warehouse=self.warehouse,
            quantity=Decimal('10'),
            performed_by=self.user,
            idempotency_key='receipt-release',
        )
        reservation = reserve_stock(
            material=self.material,
            warehouse=self.warehouse,
            quantity=Decimal('4'),
            reserved_by=self.user,
            reservation_key='reservation-002',
        )

        release_stock(reservation=reservation, released_by=self.user, release_key='release-001')

        balance = StockBalance.objects.get()
        reservation.refresh_from_db()
        self.assertEqual(reservation.status, StockReservation.Status.RELEASED)
        self.assertEqual(balance.qty_reserved, Decimal('0'))
        self.assertEqual(balance.qty_available, Decimal('10'))

    def test_transfer_moves_stock_atomically_between_warehouses(self):
        destination = Warehouse.objects.create(
            organization=self.organization,
            code='ALM-ADM',
            name='Almoxarifado Administrativo',
        )
        receive_stock(
            material=self.material,
            warehouse=self.warehouse,
            quantity=Decimal('10'),
            performed_by=self.user,
            idempotency_key='receipt-transfer',
        )

        transfer_stock(
            material=self.material,
            source=self.warehouse,
            destination=destination,
            quantity=Decimal('3'),
            performed_by=self.user,
            transfer_key='transfer-001',
        )

        source_balance = StockBalance.objects.get(warehouse=self.warehouse)
        destination_balance = StockBalance.objects.get(warehouse=destination)
        self.assertEqual(source_balance.qty_on_hand, Decimal('7'))
        self.assertEqual(destination_balance.qty_on_hand, Decimal('3'))
        self.assertEqual(StockMovement.objects.count(), 3)
