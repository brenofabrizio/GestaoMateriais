from django.core.exceptions import ValidationError
from django.db import transaction

from apps.requests.models import MaterialRequest, RequestApproval, RequestStatusHistory


def _change_status(material_request, *, new_status, changed_by, note=''):
    old_status = material_request.status
    material_request.status = new_status
    material_request.save(update_fields=('status', 'updated_at'))
    RequestStatusHistory.objects.create(
        request=material_request,
        from_status=old_status,
        to_status=new_status,
        changed_by=changed_by,
        note=note,
    )


@transaction.atomic
def submit_request(material_request, *, changed_by):
    material_request = MaterialRequest.objects.select_for_update().get(pk=material_request.pk)
    if material_request.status != MaterialRequest.Status.DRAFT:
        raise ValidationError('Somente solicitações em rascunho podem ser enviadas.')
    if not material_request.items.exists():
        raise ValidationError('A solicitação deve possuir pelo menos um item.')
    if material_request.organization_id != changed_by.organization_id:
        raise ValidationError('Usuário e solicitação pertencem a organizações diferentes.')
    _change_status(
        material_request,
        new_status=MaterialRequest.Status.PENDING_APPROVAL,
        changed_by=changed_by,
        note='Solicitação enviada para aprovação.',
    )
    return material_request


@transaction.atomic
def approve_request(material_request, *, approver, note=''):
    material_request = MaterialRequest.objects.select_for_update().get(pk=material_request.pk)
    if material_request.status != MaterialRequest.Status.PENDING_APPROVAL:
        raise ValidationError('Somente solicitações pendentes podem ser aprovadas.')
    if material_request.requester_id == approver.id:
        raise ValidationError('O solicitante não pode aprovar a própria solicitação.')
    if material_request.organization_id != approver.organization_id:
        raise ValidationError('Aprovador e solicitação pertencem a organizações diferentes.')
    if hasattr(material_request, 'approval'):
        raise ValidationError('A solicitação já possui uma decisão.')

    for item in material_request.items.select_for_update():
        item.approved_quantity = item.quantity
        item.save(update_fields=('approved_quantity',))
    RequestApproval.objects.create(
        request=material_request,
        approver=approver,
        decision=RequestApproval.Decision.APPROVED,
        note=note,
    )
    _change_status(
        material_request,
        new_status=MaterialRequest.Status.APPROVED,
        changed_by=approver,
        note=note,
    )
    return material_request


@transaction.atomic
def reject_request(material_request, *, approver, note=''):
    material_request = MaterialRequest.objects.select_for_update().get(pk=material_request.pk)
    if material_request.status != MaterialRequest.Status.PENDING_APPROVAL:
        raise ValidationError('Somente solicitações pendentes podem ser rejeitadas.')
    if not note.strip():
        raise ValidationError('A rejeição exige uma justificativa.')
    if material_request.requester_id == approver.id:
        raise ValidationError('O solicitante não pode rejeitar a própria solicitação.')
    if material_request.organization_id != approver.organization_id:
        raise ValidationError('Aprovador e solicitação pertencem a organizações diferentes.')
    if hasattr(material_request, 'approval'):
        raise ValidationError('A solicitação já possui uma decisão.')

    RequestApproval.objects.create(
        request=material_request,
        approver=approver,
        decision=RequestApproval.Decision.REJECTED,
        note=note.strip(),
    )
    _change_status(
        material_request,
        new_status=MaterialRequest.Status.REJECTED,
        changed_by=approver,
        note=note.strip(),
    )
    return material_request
