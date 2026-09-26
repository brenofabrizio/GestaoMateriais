from django.db import models

from apps.organizations.models import Organization


class MaterialCategory(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='material_categories',
    )
    code = models.CharField(max_length=60)
    name = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=('organization', 'code'),
                name='unique_material_category_code_per_organization',
            ),
        ]

    def __str__(self):
        return self.name


class Material(models.Model):
    class Kind(models.TextChoices):
        CONSUMABLE = 'consumable', 'Consumível'
        ASSET = 'asset', 'Ativo'
        SERVICE = 'service', 'Serviço'

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='materials',
    )
    category = models.ForeignKey(
        MaterialCategory,
        on_delete=models.PROTECT,
        related_name='materials',
    )
    sku = models.CharField(max_length=80)
    name = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.CONSUMABLE)
    unit = models.CharField(max_length=12, default='UN')
    minimum_stock = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    maximum_stock = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    requires_serial_number = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=('organization', 'sku'),
                name='unique_material_sku_per_organization',
            ),
            models.CheckConstraint(
                condition=models.Q(minimum_stock__gte=0),
                name='material_minimum_stock_non_negative',
            ),
            models.CheckConstraint(
                condition=models.Q(maximum_stock__gte=0),
                name='material_maximum_stock_non_negative',
            ),
        ]

    def __str__(self):
        return f'{self.sku} — {self.name}'
