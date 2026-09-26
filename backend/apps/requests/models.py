import uuid

from django.conf import settings
from django.db import models

from apps.materials.models import Material
from apps.organizations.models import Area, Organization


class MaterialRequest(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Rascunho'
        PENDING_APPROVAL = 'pending_approval', 'Aguardando aprovação'
        APPROVED = 'approved', 'Aprovada'
        REJECTED = 'rejected', 'Rejeitada'
        CANCELLED = 'cancelled', 'Cancelada'
        IN_SEPARATION = 'in_separation', 'Em separação'
        READY = 'ready', 'Pronta'
        DELIVERED = 'delivered', 'Entregue'
        COMPLETED = 'completed', 'Finalizada'

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name='material_requests')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='material_requests')
    area = models.ForeignKey(Area, on_delete=models.PROTECT, related_name='material_requests')
    code = models.CharField(max_length=32, unique=True, editable=False)
    title = models.CharField(max_length=180)
    justification = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', '-id')

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f'REQ-{uuid.uuid4().hex[:12].upper()}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.code} — {self.title}'


class RequestItem(models.Model):
    request = models.ForeignKey(MaterialRequest, on_delete=models.CASCADE, related_name='items')
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='request_items')
    quantity = models.DecimalField(max_digits=14, decimal_places=3)
    approved_quantity = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    delivered_quantity = models.DecimalField(max_digits=14, decimal_places=3, default=0)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(quantity__gt=0), name='request_item_quantity_positive'),
            models.CheckConstraint(condition=models.Q(approved_quantity__gte=0), name='request_item_approved_non_negative'),
            models.CheckConstraint(condition=models.Q(delivered_quantity__gte=0), name='request_item_delivered_non_negative'),
        ]


class RequestApproval(models.Model):
    class Decision(models.TextChoices):
        APPROVED = 'approved', 'Aprovada'
        REJECTED = 'rejected', 'Rejeitada'

    request = models.OneToOneField(MaterialRequest, on_delete=models.CASCADE, related_name='approval')
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='request_approvals')
    decision = models.CharField(max_length=20, choices=Decision.choices)
    note = models.TextField(blank=True)
    decided_at = models.DateTimeField(auto_now_add=True)


class RequestStatusHistory(models.Model):
    request = models.ForeignKey(MaterialRequest, on_delete=models.CASCADE, related_name='status_history')
    from_status = models.CharField(max_length=30, blank=True)
    to_status = models.CharField(max_length=30)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='request_status_changes')
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at', 'id')
