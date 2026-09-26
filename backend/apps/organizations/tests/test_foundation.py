from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.organizations.models import Area, Organization
from apps.accounts.models import Role


class OrganizationModelTests(TestCase):
    def test_organization_generates_slug_and_is_active_by_default(self):
        organization = Organization.objects.create(name='Empresa Exemplo')

        self.assertEqual(organization.slug, 'empresa-exemplo')
        self.assertTrue(organization.is_active)

    def test_area_code_is_unique_inside_organization(self):
        organization = Organization.objects.create(name='Empresa Exemplo')
        Area.objects.create(organization=organization, code='TI', name='Tecnologia')

        with self.assertRaises(Exception):
            Area.objects.create(organization=organization, code='TI', name='Outra TI')


class UserModelTests(TestCase):
    def test_user_is_created_with_normalized_email_and_hashed_password(self):
        organization = Organization.objects.create(name='Empresa Exemplo')
        User = get_user_model()

        user = User.objects.create_user(
            email='  ADMIN@EXEMPLO.COM ',
            password='Strong-password-123',
            organization=organization,
        )

        self.assertEqual(user.email, 'admin@exemplo.com')
        self.assertTrue(user.check_password('Strong-password-123'))
        self.assertNotEqual(user.password, 'Strong-password-123')

    def test_role_is_scoped_to_organization(self):
        organization = Organization.objects.create(name='Empresa Exemplo')
        role = Role.objects.create(
            organization=organization,
            code='AREA_MANAGER',
            name='Gestor de área',
        )

        self.assertEqual(role.organization_id, organization.id)
        self.assertEqual(str(role), 'Gestor de área')
