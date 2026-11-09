"""Entidad DetallePedido."""
from entidades.base import Base
from entidades.producto import Producto
from excepciones import CantidadInvalidaError


class DetallePedido(Base):
    """Línea de un pedido. Solo Pedido crea instancias de esta clase."""

    __cantidad: int
    __subtotal: float

    def __init__(self, cantidad: int, producto: Producto) -> None:
        super().__init__()
        self.validar_cantidad(cantidad)
        self.__cantidad = cantidad
        self.__subtotal = cantidad * producto.precio
        self.__producto: Producto = producto

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @property
    def subtotal(self) -> float:
        return self.__subtotal

    @property
    def producto(self) -> Producto:
        return self.__producto

    def sumar_cantidad(self, cantidad: int) -> None:
        """Acumula unidades al precio vigente del producto."""
        self.validar_cantidad(cantidad)
        self.__cantidad += cantidad
        self.__subtotal += cantidad * self.__producto.precio

    @staticmethod
    def validar_cantidad(cantidad: int) -> None:
        """Lanza CantidadInvalidaError si no es un entero mayor a 0."""
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise CantidadInvalidaError("La cantidad debe ser un entero mayor a 0.")

    def __str__(self) -> str:
        return f"{self.producto.nombre} x {self.cantidad} | Subtotal: ${self.subtotal:.2f}"
