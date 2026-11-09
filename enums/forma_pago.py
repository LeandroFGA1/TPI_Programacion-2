"""Formas de pago aceptadas."""
from enum import Enum


class FormaPago(Enum):
    TARJETA = "TARJETA"
    TRANSFERENCIA = "TRANSFERENCIA"
    EFECTIVO = "EFECTIVO"
