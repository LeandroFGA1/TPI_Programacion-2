"""Servicio de pedidos."""
from entidades import Pedido, Usuario
from enums import Estado, FormaPago
from excepciones import EntidadNoEncontradaError, OperacionNoPermitidaError
from servicios.producto_servicio import ProductoServicio
from servicios.servicio_base import ServicioBase
from servicios.usuario_servicio import UsuarioServicio


class PedidoServicio(ServicioBase[Pedido]):
    _nombre_entidad = "el pedido"

    def __init__(self, usuarios: UsuarioServicio, productos: ProductoServicio) -> None:
        super().__init__()
        self.__usuarios: UsuarioServicio = usuarios
        self.__productos: ProductoServicio = productos

    def iniciar(self, usuario_id: int, forma_pago: FormaPago) -> Pedido:
        """Crea un pedido en curso: todavía no está en la colección."""
        return Pedido(self.__usuarios.buscar_por_id(usuario_id), forma_pago)

    def agregar_detalle(self, pedido: Pedido, producto_id: int, cantidad: int) -> None:
        pedido.agregar_detalle(cantidad, self.__productos.buscar_por_id(producto_id))

    def quitar_detalle(self, pedido: Pedido, producto_id: int) -> None:
        pedido.eliminar_detalle_por_producto(self.__productos.buscar_por_id(producto_id))

    def registrar(self, pedido: Pedido) -> None:
        """Único punto donde el pedido se guarda y se descuenta el stock."""
        if not pedido.detalles:
            raise OperacionNoPermitidaError("El pedido debe tener al menos un detalle.")
        pedido.calcular_total()
        for detalle in pedido.detalles:
            detalle.producto.stock -= detalle.cantidad
        self._agregar(pedido)
        pedido.usuario.agregar_pedido(pedido)

    def actualizar(
        self,
        pedido_id: int,
        estado: Estado | None = None,
        forma_pago: FormaPago | None = None,
    ) -> Pedido:
        pedido = self.buscar_por_id(pedido_id)
        if estado is not None:
            pedido.estado = estado
            if estado is Estado.CANCELADO:
                self.__devolver_stock(pedido)
        if forma_pago is not None:
            pedido.forma_pago = forma_pago
        return pedido

    def eliminar(self, pedido_id: int) -> None:
        pedido = self.buscar_por_id(pedido_id)
        if pedido.estado not in (Estado.TERMINADO, Estado.CANCELADO):
            self.__devolver_stock(pedido)
        pedido.eliminar()

    def listar_de_usuario(self, usuario: Usuario) -> list[Pedido]:
        return [p for p in usuario.pedidos if not p.eliminado]

    def buscar_de_usuario(self, pedido_id: int, usuario: Usuario) -> Pedido:
        """Un pedido ajeno se informa igual que uno inexistente."""
        for pedido in self.listar_de_usuario(usuario):
            if pedido.id == pedido_id:
                return pedido
        raise EntidadNoEncontradaError(
            f"No se encontró {self._nombre_entidad} con id {pedido_id}."
        )

    @staticmethod
    def __devolver_stock(pedido: Pedido) -> None:
        for detalle in pedido.detalles:
            detalle.producto.stock += detalle.cantidad
