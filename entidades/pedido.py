"""Entidad Pedido."""
from datetime import date

from entidades.base import Base
from entidades.calculable import Calculable
from entidades.detalle_pedido import DetallePedido
from entidades.producto import Producto
from entidades.usuario import Usuario
from enums import Estado, FormaPago
from excepciones import (
    DatoInvalidoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    StockInsuficienteError,
)


class Pedido(Base, Calculable):
    """Pedido de un usuario; compone sus detalles (nacen y mueren con él)."""

    __forma_pago: FormaPago

    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        super().__init__()
        if not isinstance(usuario, Usuario):
            raise DatoInvalidoError("El pedido debe tener un usuario.")
        if usuario.eliminado:
            raise EntidadNoEncontradaError("El usuario no existe o está eliminado.")
        self.__usuario: Usuario = usuario
        self.__fecha: date = date.today()
        self.__estado: Estado = Estado.PENDIENTE
        self.__total: float = 0.0
        self.__detalles: list[DetallePedido] = []
        self.forma_pago = forma_pago

    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def total(self) -> float:
        return self.__total

    @property
    def estado(self) -> Estado:
        return self.__estado

    @estado.setter
    def estado(self, valor: Estado) -> None:
        if not isinstance(valor, Estado):
            raise DatoInvalidoError("El estado no es válido.")
        if not self.__estado.puede_pasar_a(valor):
            raise OperacionNoPermitidaError(
                f"Transición inválida: {self.__estado.value} -> {valor.value}."
            )
        self.__estado = valor

    @property
    def forma_pago(self) -> FormaPago:
        return self.__forma_pago

    @forma_pago.setter
    def forma_pago(self, valor: FormaPago) -> None:
        if not isinstance(valor, FormaPago):
            raise DatoInvalidoError("La forma de pago no es válida.")
        self.__forma_pago = valor

    @property
    def detalles(self) -> tuple[DetallePedido, ...]:
        """Copia inmutable de los detalles vigentes."""
        return tuple(d for d in self.__detalles if not d.eliminado)

    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        """Agrega un producto o acumula la cantidad si ya estaba en el pedido."""
        self.__validar_modificable()
        self.__validar_producto(producto)
        DetallePedido.validar_cantidad(cantidad)
        existente = self.buscar_detalle_por_producto(producto)
        if existente is None:
            self.__validar_stock(cantidad, producto)
            self.__detalles.append(DetallePedido(cantidad, producto))
        else:
            self.__validar_stock(existente.cantidad + cantidad, producto)
            existente.sumar_cantidad(cantidad)
        self.calcular_total()

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        """Devuelve el detalle vigente del producto o None."""
        for detalle in self.detalles:
            if detalle.producto == producto:
                return detalle
        return None

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        """Da de baja lógica el detalle del producto y recalcula el total."""
        self.__validar_modificable()
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle is None:
            raise EntidadNoEncontradaError(f"{producto.nombre} no está en el pedido.")
        detalle.eliminar()
        self.calcular_total()

    def calcular_total(self) -> None:
        """Suma los subtotales; un pedido dado de baja conserva su total."""
        if not self.eliminado:
            self.__total = sum(d.subtotal for d in self.detalles)

    def eliminar(self) -> None:
        """Baja lógica en cascada: incluye a los detalles (composición)."""
        for detalle in self.__detalles:
            detalle.eliminar()
        super().eliminar()

    def __validar_modificable(self) -> None:
        if self.eliminado or self.__estado is not Estado.PENDIENTE:
            raise OperacionNoPermitidaError("Solo se modifica un pedido PENDIENTE.")

    @staticmethod
    def __validar_producto(producto: Producto) -> None:
        if not isinstance(producto, Producto) or producto.eliminado:
            raise EntidadNoEncontradaError("El producto no existe o está eliminado.")
        if not producto.disponible:
            raise OperacionNoPermitidaError(f"{producto.nombre} no está disponible.")

    @staticmethod
    def __validar_stock(cantidad: int, producto: Producto) -> None:
        if cantidad > producto.stock:
            raise StockInsuficienteError(
                f"Stock insuficiente de {producto.nombre}: "
                f"pedido {cantidad}, disponible {producto.stock}."
            )

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.usuario.nombre_completo} | {self.estado.value} "
            f"| {self.forma_pago.value} | Total: ${self.total:.2f} | {self.fecha:%d/%m/%Y}"
        )
