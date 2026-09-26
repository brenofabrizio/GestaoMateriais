from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.inventory.models import StockBalance, StockMovement


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
        material=material,
        warehouse=warehouse,
        kind=StockMovement.Kind.RECEIPT,
        quantity=quantity,
        balance_after=balance.qty_on_hand,
        performed_by=performed_by,
        idempotency_key=idempotency_key,
        note=note,
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
        material=material,
        warehouse=warehouse,
        kind=StockMovement.Kind.ISSUE,
        quantity=quantity,
        balance_after=balance.qty_on_hand,
        performed_by=performed_by,
        idempotency_key=idempotency_key,
        note=note,
    )
