from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.inventory.models import StockBalance, StockMovement, StockReservation


def _validate_quantity(quantity):
    quantity = Decimal(str(quantity))
    if quantity <= 0:
        raise ValidationError('A quantidade deve ser maior que zero.')
    return quantity


def _get_or_create_balance(material, warehouse):
    balance, _ = StockBalance.objects.select_for_update().get_or_create(
        material=material,
        warehouse=warehouse,
    )
    return balance


def _existing_idempotent_movement(idempotency_key):
    if not idempotency_key:
        raise ValidationError('A chave de idempotência é obrigatória.')
    return StockMovement.objects.filter(idempotency_key=idempotency_key).first()


@transaction.atomic
def receive_stock(*, material, warehouse, quantity, performed_by, idempotency_key, note=''):
    existing = _existing_idempotent_movement(idempotency_key)
    if existing:
        return existing
    quantity = _validate_quantity(quantity)
    balance = _get_or_create_balance(material, warehouse)
    balance.qty_on_hand += quantity
    balance.save(update_fields=('qty_on_hand', 'updated_at'))
    return StockMovement.objects.create(
        material=material, warehouse=warehouse, kind=StockMovement.Kind.RECEIPT,
        quantity=quantity, balance_after=balance.qty_on_hand, performed_by=performed_by,
        idempotency_key=idempotency_key, note=note,
    )


@transaction.atomic
def issue_stock(*, material, warehouse, quantity, performed_by, idempotency_key, note=''):
    existing = _existing_idempotent_movement(idempotency_key)
    if existing:
        return existing
    quantity = _validate_quantity(quantity)
    balance = _get_or_create_balance(material, warehouse)
    if balance.qty_available < quantity:
        raise ValidationError('Estoque disponível insuficiente para esta saída.')
    balance.qty_on_hand -= quantity
    balance.save(update_fields=('qty_on_hand', 'updated_at'))
    return StockMovement.objects.create(
        material=material, warehouse=warehouse, kind=StockMovement.Kind.ISSUE,
        quantity=quantity, balance_after=balance.qty_on_hand, performed_by=performed_by,
        idempotency_key=idempotency_key, note=note,
    )


@transaction.atomic
def reserve_stock(*, material, warehouse, quantity, reserved_by, reservation_key, note=''):
    existing = StockReservation.objects.filter(reservation_key=reservation_key).first()
    if existing:
        return existing
    quantity = _validate_quantity(quantity)
    balance = _get_or_create_balance(material, warehouse)
    if balance.qty_available < quantity:
        raise ValidationError('Estoque disponível insuficiente para esta reserva.')
    balance.qty_reserved += quantity
    balance.save(update_fields=('qty_reserved', 'updated_at'))
    StockMovement.objects.create(
        material=material, warehouse=warehouse, kind=StockMovement.Kind.RESERVATION,
        quantity=quantity, balance_after=balance.qty_on_hand, performed_by=reserved_by,
        idempotency_key=f'{reservation_key}:reserve', note=note,
    )
    return StockReservation.objects.create(
        material=material, warehouse=warehouse, quantity=quantity,
        reserved_by=reserved_by, reservation_key=reservation_key,
    )


@transaction.atomic
def release_stock(*, reservation, released_by, release_key, note=''):
    reservation = StockReservation.objects.select_for_update().select_related('material', 'warehouse').get(pk=reservation.pk)
    if reservation.status != StockReservation.Status.ACTIVE:
        return reservation
    existing = _existing_idempotent_movement(f'{release_key}:release')
    if existing:
        return reservation
    balance = _get_or_create_balance(reservation.material, reservation.warehouse)
    if balance.qty_reserved < reservation.quantity:
        raise ValidationError('A reserva excede o saldo reservado atual.')
    balance.qty_reserved -= reservation.quantity
    balance.save(update_fields=('qty_reserved', 'updated_at'))
    StockMovement.objects.create(
        material=reservation.material, warehouse=reservation.warehouse, kind=StockMovement.Kind.RELEASE,
        quantity=reservation.quantity, balance_after=balance.qty_on_hand, performed_by=released_by,
        idempotency_key=f'{release_key}:release', note=note,
    )
    reservation.status = StockReservation.Status.RELEASED
    reservation.released_at = timezone.now()
    reservation.save(update_fields=('status', 'released_at'))
    return reservation


@transaction.atomic
def transfer_stock(*, material, source, destination, quantity, performed_by, transfer_key, note=''):
    if source.pk == destination.pk:
        raise ValidationError('A origem e o destino da transferência devem ser diferentes.')
    existing = StockMovement.objects.filter(idempotency_key=f'{transfer_key}:out').first()
    if existing:
        return existing
    quantity = _validate_quantity(quantity)
    source_balance = _get_or_create_balance(material, source)
    if source_balance.qty_available < quantity:
        raise ValidationError('Estoque disponível insuficiente para esta transferência.')
    destination_balance = _get_or_create_balance(material, destination)
    source_balance.qty_on_hand -= quantity
    destination_balance.qty_on_hand += quantity
    source_balance.save(update_fields=('qty_on_hand', 'updated_at'))
    destination_balance.save(update_fields=('qty_on_hand', 'updated_at'))
    StockMovement.objects.create(
        material=material, warehouse=source, kind=StockMovement.Kind.TRANSFER_OUT,
        quantity=quantity, balance_after=source_balance.qty_on_hand, performed_by=performed_by,
        idempotency_key=f'{transfer_key}:out', reference_type='transfer', reference_id=transfer_key, note=note,
    )
    return StockMovement.objects.create(
        material=material, warehouse=destination, kind=StockMovement.Kind.TRANSFER_IN,
        quantity=quantity, balance_after=destination_balance.qty_on_hand, performed_by=performed_by,
        idempotency_key=f'{transfer_key}:in', reference_type='transfer', reference_id=transfer_key, note=note,
    )
