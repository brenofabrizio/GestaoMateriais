from django.conf import settings
from django.db import models

from apps.materials.models import Material
from apps.organizations.models import Organization


class Warehouse(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='warehouses',
    )
    code = models.CharField(max_length=60)
    name = models.CharField(max_length=140)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=('organization', 'code'),
                name='unique_warehouse_code_per_organization',
            ),
        ]

    def __str__(self):
        return self.name


class StockBalance(models.Model):
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='stock_balances')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='stock_balances')
    qty_on_hand = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    qty_reserved = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('material', 'warehouse'),
                name='unique_stock_balance_per_material_warehouse',
            ),
            models.CheckConstraint(
                condition=models.Q(qty_on_hand__gte=0),
                name='stock_on_hand_non_negative',
            ),
            models.CheckConstraint(
                condition=models.Q(qty_reserved__gte=0),
                name='stock_reserved_non_negative',
            ),
        ]

    @property
    def qty_available(self):
        return self.qty_on_hand - self.qty_reserved


class StockMovement(models.Model):
    class Kind(models.TextChoices):
        RECEIPT = 'receipt', 'Entrada'
        ISSUE = 'issue', 'Saída'
        ADJUSTMENT = 'adjustment', 'Ajuste'
        TRANSFER_IN = 'transfer_in', 'Transferência recebida'
        TRANSFER_OUT = 'transfer_out', 'Transferência enviada'
        RESERVATION = 'reservation', 'Reserva'
        RELEASE = 'release', 'Liberação'

    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='stock_movements')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='stock_movements')
    kind = models.CharField(max_length=20, choices=Kind.choices)
    quantity = models.DecimalField(max_digits=14, decimal_places=3)
    balance_after = models.DecimalField(max_digits=14, decimal_places=3)
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='stock_movements',
    )
    idempotency_key = models.CharField(max_length=180, unique=True)
    reference_type = models.CharField(max_length=80, blank=True)
    reference_id = models.CharField(max_length=80, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', '-id')
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0),
                name='stock_movement_quantity_positive',
            ),
            models.CheckConstraint(
                condition=models.Q(balance_after__gte=0),
                name='stock_movement_balance_non_negative',
            ),
        ]

    def __str__(self):
        return f'{self.get_kind_display()} {self.quantity} — {self.material.sku}'
