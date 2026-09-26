from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.accounts.models import User
from apps.materials.models import Material, MaterialCategory
from apps.organizations.models import Area, Organization
from apps.requests.models import MaterialRequest, RequestApproval, RequestItem, RequestStatusHistory
from apps.requests.services import approve_request, reject_request, submit_request


class RequestWorkflowTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name='Empresa Exemplo')
        self.area = Area.objects.create(
            organization=self.organization,
            code='ADM',
            name='Administrativo',
        )
        category = MaterialCategory.objects.create(
            organization=self.organization,
            code='PAPELARIA',
            name='Papelaria',
        )
        self.material = Material.objects.create(
            organization=self.organization,
            category=category,
            sku='ADM-CANETA-001',
            name='Caneta azul',
        )
        self.requester = User.objects.create_user(
            email='solicitante@exemplo.com',
            password='Strong-password-123',
            organization=self.organization,
            area=self.area,
        )
        self.approver = User.objects.create_user(
            email='gestor@exemplo.com',
            password='Strong-password-123',
            organization=self.organization,
            area=self.area,
        )

    def create_request(self):
        material_request = MaterialRequest.objects.create(
            organization=self.organization,
            requester=self.requester,
            area=self.area,
            title='Materiais para o setor',
            justification='Reposição mensal',
        )
        RequestItem.objects.create(
            request=material_request,
            material=self.material,
            quantity=Decimal('10'),
        )
        return material_request

    def test_submit_requires_at_least_one_item(self):
        material_request = MaterialRequest.objects.create(
            organization=self.organization,
            requester=self.requester,
            area=self.area,
            title='Solicitação vazia',
        )

        with self.assertRaises(ValidationError):
            submit_request(material_request, changed_by=self.requester)

    def test_submit_moves_request_to_pending_approval_and_creates_history(self):
        material_request = self.create_request()

        submit_request(material_request, changed_by=self.requester)

        material_request.refresh_from_db()
        self.assertEqual(material_request.status, MaterialRequest.Status.PENDING_APPROVAL)
        self.assertEqual(RequestStatusHistory.objects.filter(request=material_request).count(), 1)

    def test_requester_cannot_approve_own_request(self):
        material_request = self.create_request()
        submit_request(material_request, changed_by=self.requester)

        with self.assertRaises(ValidationError):
            approve_request(material_request, approver=self.requester)

    def test_approver_approves_request_and_records_decision(self):
        material_request = self.create_request()
        submit_request(material_request, changed_by=self.requester)

        approve_request(material_request, approver=self.approver, note='Aprovado pelo gestor')

        material_request.refresh_from_db()
        item = material_request.items.get()
        approval = RequestApproval.objects.get(request=material_request)
        self.assertEqual(material_request.status, MaterialRequest.Status.APPROVED)
        self.assertEqual(item.approved_quantity, Decimal('10'))
        self.assertEqual(approval.decision, RequestApproval.Decision.APPROVED)
        self.assertEqual(RequestStatusHistory.objects.filter(request=material_request).count(), 2)

    def test_rejection_requires_reason_and_records_rejection(self):
        material_request = self.create_request()
        submit_request(material_request, changed_by=self.requester)

        with self.assertRaises(ValidationError):
            reject_request(material_request, approver=self.approver, note='')

        reject_request(material_request, approver=self.approver, note='Fora do orçamento')
        material_request.refresh_from_db()
        self.assertEqual(material_request.status, MaterialRequest.Status.REJECTED)
