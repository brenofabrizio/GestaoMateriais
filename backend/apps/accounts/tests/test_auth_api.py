from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.accounts.models import Role, UserRole
from apps.organizations.models import Area, Organization


class AuthenticationApiTests(APITestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name='Empresa Exemplo')
        self.area = Area.objects.create(
            organization=self.organization,
            code='TI',
            name='Tecnologia',
        )
        self.user = User.objects.create_user(
            email='admin@exemplo.com',
            password='Strong-password-123',
            first_name='Admin',
            organization=self.organization,
            area=self.area,
        )
        self.role = Role.objects.create(
            organization=self.organization,
            code='AREA_MANAGER',
            name='Gestor de área',
        )
        UserRole.objects.create(user=self.user, role=self.role)

    def test_user_can_login_and_access_me(self):
        response = self.client.post(
            reverse('auth-token'),
            {'email': 'admin@exemplo.com', 'password': 'Strong-password-123'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        me_response = self.client.get(reverse('auth-me'))

        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
        self.assertEqual(me_response.data['email'], 'admin@exemplo.com')
        self.assertEqual(me_response.data['organization']['slug'], 'empresa-exemplo')
        self.assertEqual(me_response.data['area']['code'], 'TI')
        self.assertEqual(me_response.data['roles'][0]['code'], 'AREA_MANAGER')

    def test_invalid_credentials_are_rejected(self):
        response = self.client.post(
            reverse('auth-token'),
            {'email': 'admin@exemplo.com', 'password': 'wrong-password'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_requires_authentication(self):
        response = self.client.get(reverse('auth-me'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_blacklists_refresh_token(self):
        login_response = self.client.post(
            reverse('auth-token'),
            {'email': 'admin@exemplo.com', 'password': 'Strong-password-123'},
            format='json',
        )
        refresh = login_response.data['refresh']

        logout_response = self.client.post(
            reverse('auth-logout'),
            {'refresh': refresh},
            format='json',
        )
        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)

        refresh_response = self.client.post(
            reverse('auth-token-refresh'),
            {'refresh': refresh},
            format='json',
        )
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
