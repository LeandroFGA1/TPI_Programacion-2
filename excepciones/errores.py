"""Jerarquía de excepciones: todas heredan de FoodStoreError."""


class FoodStoreError(Exception):
    """Raíz de los errores de negocio; la consola la captura para informar."""


class EntidadNoEncontradaError(FoodStoreError):
    """El id no existe o la entidad está eliminada."""


class DatoInvalidoError(FoodStoreError):
    """Texto vacío, formato incorrecto o tipo inesperado."""


class PrecioInvalidoError(DatoInvalidoError):
    """El precio es negativo o no es un número finito."""


class StockInvalidoError(DatoInvalidoError):
    """El stock es negativo o no es un entero."""


class CantidadInvalidaError(DatoInvalidoError):
    """La cantidad de un detalle no es un entero mayor a cero."""


class StockInsuficienteError(FoodStoreError):
    """La cantidad pedida supera el stock del producto."""


class DuplicadoError(FoodStoreError):
    """Mail o nombre de categoría repetido."""


class OperacionNoPermitidaError(FoodStoreError):
    """La operación viola una regla de negocio."""


class CredencialesInvalidasError(FoodStoreError):
    """Mail o contraseña incorrectos, o usuario eliminado."""
