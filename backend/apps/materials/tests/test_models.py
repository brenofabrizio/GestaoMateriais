from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from apps.materials.models import Material, MaterialCategory
from apps.organizations.models import Organization


class MaterialCatalogTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name='Empresa Exemplo')
        self.category = MaterialCategory.objects.create(
            organization=self.organization,
            code='PERIFERICOS',
            name='Periféricos',
        )

    def test_category_code_is_unique_per_organization(self):
        with self.assertRaises(IntegrityError):
            MaterialCategory.objects.create(
                organization=self.organization,
                code='PERIFERICOS',
                name='Outra categoria',
            )

    def test_material_has_safe_defaults_for_stock_policy(self):
        material = Material.objects.create(
            organization=self.organization,
            category=self.category,
            sku='TI-MOUSE-001',
            name='Mouse sem fio',
            unit='UN',
        )

        self.assertEqual(material.kind, Material.Kind.CONSUMABLE)
        self.assertEqual(material.minimum_stock, Decimal('0'))
        self.assertEqual(material.maximum_stock, Decimal('0'))
        self.assertTrue(material.is_active)

    def test_sku_is_unique_per_organization(self):
        Material.objects.create(
            organization=self.organization,
            category=self.category,
            sku='TI-MOUSE-001',
            name='Mouse sem fio',
            unit='UN',
        )

        with self.assertRaises(IntegrityError):
            Material.objects.create(
                organization=self.organization,
                category=self.category,
                sku='TI-MOUSE-001',
                name='Mouse reserva',
                unit='UN',
            )
