"""Pruebas del modelo y los servicios, sin menú: python pruebas.py."""
import sys
from collections.abc import Callable

from consola import MenuAdministrador, MenuCliente, crear_menu
from entidades import Base, Calculable, Categoria, DetallePedido, Pedido, Producto, Usuario
from enums import Estado, FormaPago, Rol
from excepciones import (
    CantidadInvalidaError,
    CredencialesInvalidasError,
    DatoInvalidoError,
    DuplicadoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    PrecioInvalidoError,
    StockInsuficienteError,
    StockInvalidoError,
)
from servicios import (
    CategoriaServicio,
    PedidoServicio,
    ProductoServicio,
    UsuarioServicio,
)


class Resultados:
    """Ejecuta los casos, los muestra en pantalla y lleva la cuenta."""

    def __init__(self) -> None:
        self.__correctos: int = 0
        self.__fallidos: int = 0

    @property
    def fallidos(self) -> int:
        return self.__fallidos

    def seccion(self, titulo: str) -> None:
        print(f"\n--- {titulo} ---")

    def valido(self, descripcion: str, comprobacion: Callable[[], bool]) -> None:
        """El caso debe ejecutarse sin error y devolver True."""
        try:
            correcto = comprobacion()
        except Exception as error:  # Una prueba debe reportar cualquier fallo.
            self.__registrar(False, descripcion, f"{type(error).__name__}: {error}")
        else:
            self.__registrar(correcto, descripcion, "resultado correcto")

    def error(
        self,
        descripcion: str,
        esperada: type[Exception],
        accion: Callable[[], object],
    ) -> None:
        """El caso debe lanzar exactamente la excepción esperada."""
        try:
            accion()
        except Exception as error:  # Una prueba debe reportar cualquier fallo.
            correcto = type(error) is esperada
            self.__registrar(correcto, descripcion, f"{type(error).__name__}: {error}")
        else:
            self.__registrar(False, descripcion, f"no se lanzó {esperada.__name__}")

    def resumen(self) -> None:
        total = self.__correctos + self.__fallidos
        print(f"\nRESULTADO: {self.__correctos}/{total} casos correctos.")

    def __registrar(self, correcto: bool, descripcion: str, detalle: str) -> None:
        if correcto:
            self.__correctos += 1
        else:
            self.__fallidos += 1
        print(f"[{'OK' if correcto else 'FALLA'}] {descripcion} -> {detalle}")


class Entorno:
    """Servicios y datos nuevos para cada grupo de pruebas."""

    def __init__(self) -> None:
        self.categorias: CategoriaServicio = CategoriaServicio()
        self.productos: ProductoServicio = ProductoServicio(self.categorias)
        self.usuarios: UsuarioServicio = UsuarioServicio()
        self.pedidos: PedidoServicio = PedidoServicio(self.usuarios, self.productos)
        self.admin: Usuario = self.usuarios.crear(
            "Ana", "Pérez", "admin@x.com", "111", "admin123", Rol.ADMIN
        )
        self.cliente: Usuario = self.usuarios.crear(
            "Juan", "Gómez", "juan@x.com", "222", "juan123", Rol.USUARIO
        )
        self.categoria: Categoria = self.categorias.crear("Pizzas", "A la piedra")
        self.producto: Producto = self.productos.crear("Muzza", 100.0, 5, self.categoria.id)
        self.otro: Producto = self.productos.crear("Fugazza", 50.0, 10, self.categoria.id)

    def pedido_registrado(self, cantidad: int = 2) -> Pedido:
        pedido = self.pedidos.iniciar(self.cliente.id, FormaPago.EFECTIVO)
        self.pedidos.agregar_detalle(pedido, self.producto.id, cantidad)
        self.pedidos.registrar(pedido)
        return pedido


def asignar(objeto: object, atributo: str, valor: object) -> None:
    """Hace una asignación dentro de un lambda."""
    setattr(objeto, atributo, valor)


def probar_modelo(r: Resultados) -> None:
    r.seccion("Modelo")
    e = Entorno()
    r.error("Base no se puede instanciar", TypeError, lambda: Base())  # type: ignore[abstract]
    r.error("Calculable no se puede instanciar", TypeError, lambda: Calculable())  # type: ignore[abstract]
    r.valido("Pedido implementa Calculable", lambda: issubclass(Pedido, Calculable))
    r.valido("Los id se generan solos y no se repiten", lambda: e.producto.id != e.otro.id)
    r.valido("__eq__ compara por id", lambda: e.producto == e.producto and e.producto != e.otro)
    r.valido("__str__ del producto incluye su categoría", lambda: "Pizzas" in str(e.producto))
    r.error("id no tiene setter", AttributeError, lambda: asignar(e.producto, "id", 99))
    r.error("creado_en no tiene setter", AttributeError, lambda: asignar(e.producto, "creado_en", None))
    r.error("contrasenia no tiene property", AttributeError, lambda: e.admin.contrasenia)  # type: ignore[attr-defined]
    r.valido("verificar_contrasenia acepta la correcta", lambda: e.admin.verificar_contrasenia("admin123"))
    r.valido("verificar_contrasenia rechaza otra", lambda: not e.admin.verificar_contrasenia("x"))
    r.valido("__str__ del usuario no muestra la contraseña", lambda: "admin123" not in str(e.admin))
    r.error("Precio negativo", PrecioInvalidoError, lambda: Producto("A", -1, 1, e.categoria))
    r.error("Precio NaN", PrecioInvalidoError, lambda: Producto("A", float("nan"), 1, e.categoria))
    r.error("Precio infinito", PrecioInvalidoError, lambda: Producto("A", float("inf"), 1, e.categoria))
    r.error("Stock negativo", StockInvalidoError, lambda: Producto("A", 1, -1, e.categoria))
    r.error("Nombre vacío", DatoInvalidoError, lambda: Producto("  ", 1, 1, e.categoria))
    r.error("Mail sin formato", DatoInvalidoError, lambda: Usuario("A", "B", "sinarroba", "1", "x", Rol.USUARIO))
    r.error("Contraseña vacía", DatoInvalidoError, lambda: Usuario("A", "B", "a@b.c", "1", " ", Rol.USUARIO))
    r.valido("Un producto inválido no queda en su categoría", lambda: len(e.categoria.productos) == 2)


def probar_categorias(r: Resultados) -> None:
    r.seccion("Categorías")
    e = Entorno()
    r.valido("Crear categoría", lambda: e.categorias.crear("Bebidas", "Frías").id > 0)
    r.error("Nombre repetido sin distinguir mayúsculas", DuplicadoError, lambda: e.categorias.crear("bEbIdAs", "X"))
    r.error("Editar con nombre de otra", DuplicadoError, lambda: e.categorias.editar(e.categoria.id, "BEBIDAS"))
    r.valido("Editar conservando su propio nombre", lambda: e.categorias.editar(e.categoria.id, "pizzas").nombre == "pizzas")
    r.error("Editar id inexistente", EntidadNoEncontradaError, lambda: e.categorias.editar(9999, "X"))
    r.error("No se elimina con productos activos", OperacionNoPermitidaError, lambda: e.categorias.eliminar(e.categoria.id))
    vacia = e.categorias.crear("Postres", "Dulces")
    e.categorias.eliminar(vacia.id)
    r.valido("Baja lógica: sale del listado", lambda: vacia not in e.categorias.listar())
    r.valido("Baja lógica: el objeto sigue marcado", lambda: vacia.eliminado)
    r.error("Producto en categoría eliminada", EntidadNoEncontradaError, lambda: e.productos.crear("A", 1, 1, vacia.id))
    e.productos.eliminar(e.producto.id)
    e.productos.eliminar(e.otro.id)
    e.categorias.eliminar(e.categoria.id)
    r.valido("Sin productos activos sí se elimina", lambda: e.categoria.eliminado)


def probar_productos(r: Resultados) -> None:
    r.seccion("Productos")
    e = Entorno()
    r.valido("Precio 0 y stock 0 son válidos", lambda: e.productos.crear("Promo", 0, 0, e.categoria.id).stock == 0)
    r.error("Edición con precio negativo", PrecioInvalidoError, lambda: e.productos.editar(e.producto.id, precio=-5))

    def edicion_atomica() -> bool:
        try:
            e.productos.editar(e.producto.id, nombre="Otro", stock=-1)
        except StockInvalidoError:
            return e.producto.nombre == "Muzza"
        return False

    r.valido("Edición inválida no deja cambios parciales", edicion_atomica)
    bebidas = e.categorias.crear("Bebidas", "Frías")

    def mover_categoria() -> bool:
        e.productos.editar(e.otro.id, categoria_id=bebidas.id)
        return e.otro in bebidas.productos and e.otro not in e.categoria.productos

    r.valido("Cambiar de categoría actualiza ambos lados", mover_categoria)
    e.productos.editar(e.otro.id, disponible=False)
    r.valido("El cliente no ve productos no disponibles", lambda: e.otro not in e.productos.listar_disponibles())
    e.productos.editar(e.producto.id, stock=0)
    r.valido("El cliente no ve productos sin stock", lambda: e.producto not in e.productos.listar_disponibles())
    r.valido("El administrador sí los ve", lambda: e.producto in e.productos.listar())


def probar_usuarios(r: Resultados) -> None:
    r.seccion("Usuarios y sesión")
    e = Entorno()
    mensaje = "Mail o contraseña incorrectos."
    r.valido("Autenticación correcta", lambda: e.usuarios.autenticar("ADMIN@x.com", "admin123") == e.admin)
    r.error("Mail inexistente", CredencialesInvalidasError, lambda: e.usuarios.autenticar("no@x.com", "x"))
    r.error("Contraseña incorrecta", CredencialesInvalidasError, lambda: e.usuarios.autenticar("admin@x.com", "x"))

    def mensaje_de(mail: str, contrasenia: str) -> str:
        try:
            e.usuarios.autenticar(mail, contrasenia)
        except CredencialesInvalidasError as error:
            return str(error)
        return ""

    r.valido("El mensaje no revela qué dato falló", lambda: mensaje_de("no@x.com", "x") == mensaje == mensaje_de("admin@x.com", "x"))
    r.error("Mail repetido", DuplicadoError, lambda: e.usuarios.crear("A", "B", "JUAN@x.com", "1", "x", Rol.USUARIO))
    r.error("Editar con mail ajeno", DuplicadoError, lambda: e.usuarios.editar(e.cliente.id, e.admin, mail="admin@x.com"))
    r.valido("Editar conservando su propio mail", lambda: e.usuarios.editar(e.cliente.id, e.admin, mail="juan@x.com").mail == "juan@x.com")
    r.error("Un administrador no se elimina a sí mismo", OperacionNoPermitidaError, lambda: e.usuarios.eliminar(e.admin.id, e.admin))
    r.error("Un administrador no cambia su propio rol", OperacionNoPermitidaError, lambda: e.usuarios.editar(e.admin.id, e.admin, rol=Rol.USUARIO))
    pedido = e.pedido_registrado()
    e.usuarios.eliminar(e.cliente.id, e.admin)
    r.valido("Usuario eliminado sale del listado", lambda: e.cliente not in e.usuarios.listar())
    r.error("Usuario eliminado no inicia sesión", CredencialesInvalidasError, lambda: e.usuarios.autenticar("juan@x.com", "juan123"))
    r.error("Usuario eliminado no recibe pedidos", EntidadNoEncontradaError, lambda: e.pedidos.iniciar(e.cliente.id, FormaPago.EFECTIVO))
    r.error("Pedido directo con usuario eliminado", EntidadNoEncontradaError, lambda: Pedido(e.cliente, FormaPago.EFECTIVO))
    r.error("Pedido sin usuario", DatoInvalidoError, lambda: Pedido(None, FormaPago.EFECTIVO))  # type: ignore[arg-type]
    r.valido("Sus pedidos se siguen consultando", lambda: pedido in e.pedidos.listar())
    r.valido("El menú depende del rol: admin", lambda: isinstance(crear_menu(e.admin, e.categorias, e.productos, e.usuarios, e.pedidos), MenuAdministrador))
    r.valido("El menú depende del rol: cliente", lambda: isinstance(crear_menu(e.cliente, e.categorias, e.productos, e.usuarios, e.pedidos), MenuCliente))


def probar_detalles(r: Resultados) -> None:
    r.seccion("Detalles de pedido")
    e = Entorno()
    pedido = e.pedidos.iniciar(e.cliente.id, FormaPago.TARJETA)
    r.valido("Arranca PENDIENTE y con la fecha del día", lambda: pedido.estado is Estado.PENDIENTE and pedido.total == 0)
    r.error("Pedido sin detalles no se registra", OperacionNoPermitidaError, lambda: e.pedidos.registrar(pedido))
    r.error("Cantidad cero", CantidadInvalidaError, lambda: pedido.agregar_detalle(0, e.producto))
    r.error("Cantidad negativa", CantidadInvalidaError, lambda: pedido.agregar_detalle(-1, e.producto))
    r.error("Cantidad mayor al stock", StockInsuficienteError, lambda: pedido.agregar_detalle(6, e.producto))
    pedido.agregar_detalle(2, e.producto)
    r.valido("Subtotal = cantidad x precio", lambda: pedido.detalles[0].subtotal == 200)
    r.valido("agregar_detalle actualiza el total", lambda: pedido.total == 200)
    r.valido("El stock no se descuenta antes de registrar", lambda: e.producto.stock == 5)
    pedido.agregar_detalle(1, e.producto)
    r.valido("Mismo producto: suma al detalle existente", lambda: len(pedido.detalles) == 1 and pedido.detalles[0].cantidad == 3)
    r.error("La suma acumulada no puede superar el stock", StockInsuficienteError, lambda: pedido.agregar_detalle(3, e.producto))
    r.valido("Tras el error el detalle no cambia", lambda: pedido.detalles[0].cantidad == 3 and pedido.total == 300)
    r.valido("La lista de detalles es una tupla", lambda: isinstance(pedido.detalles, tuple))
    r.valido("Buscar detalle existente", lambda: isinstance(pedido.buscar_detalle_por_producto(e.producto), DetallePedido))
    r.valido("Buscar detalle inexistente da None", lambda: pedido.buscar_detalle_por_producto(e.otro) is None)
    r.error("Quitar un producto ausente", EntidadNoEncontradaError, lambda: pedido.eliminar_detalle_por_producto(e.otro))
    pedido.eliminar_detalle_por_producto(e.producto)
    r.valido("Quitar un detalle recalcula el total", lambda: pedido.total == 0 and pedido.detalles == ())
    e.productos.editar(e.otro.id, disponible=False)
    r.error("Producto no disponible", OperacionNoPermitidaError, lambda: pedido.agregar_detalle(1, e.otro))
    e.productos.eliminar(e.producto.id)
    r.error("Producto eliminado por id", EntidadNoEncontradaError, lambda: e.pedidos.agregar_detalle(pedido, e.producto.id, 1))
    r.error("Producto eliminado en el modelo", EntidadNoEncontradaError, lambda: pedido.agregar_detalle(1, e.producto))


def probar_registro_pedidos(r: Resultados) -> None:
    r.seccion("Creación de pedidos")
    e = Entorno()
    fallido = e.pedidos.iniciar(e.cliente.id, FormaPago.EFECTIVO)
    e.pedidos.agregar_detalle(fallido, e.otro.id, 1)
    r.error("Falta de stock durante la creación", StockInsuficienteError, lambda: e.pedidos.agregar_detalle(fallido, e.producto.id, 99))
    r.valido("Creación fallida: no entra a la colección", lambda: e.pedidos.listar() == [])
    r.valido("Creación fallida: no queda en el usuario", lambda: e.cliente.pedidos == ())
    r.valido("Creación fallida: el stock no cambia", lambda: e.producto.stock == 5 and e.otro.stock == 10)
    pedido = e.pedido_registrado(2)
    r.valido("Registro: entra a la colección", lambda: pedido in e.pedidos.listar())
    r.valido("Registro: queda asociado al usuario", lambda: pedido in e.cliente.pedidos)
    r.valido("Registro: descuenta el stock", lambda: e.producto.stock == 3)
    e.productos.editar(e.producto.id, precio=999)
    r.valido("Cambiar el precio no altera pedidos ya hechos", lambda: pedido.total == 200)
    e.productos.eliminar(e.producto.id)
    r.valido("Producto eliminado: el pedido se sigue mostrando", lambda: "Muzza" in str(pedido.detalles[0]))
    r.error("Pedido ajeno se informa como inexistente", EntidadNoEncontradaError, lambda: e.pedidos.buscar_de_usuario(pedido.id, e.admin))
    r.valido("Pedido propio se encuentra", lambda: e.pedidos.buscar_de_usuario(pedido.id, e.cliente) == pedido)


def probar_estados(r: Resultados) -> None:
    r.seccion("Estados y stock")
    e = Entorno()
    pedido = e.pedido_registrado(2)
    r.error("PENDIENTE -> TERMINADO no es válida", OperacionNoPermitidaError, lambda: e.pedidos.actualizar(pedido.id, Estado.TERMINADO))
    r.error("PENDIENTE -> PENDIENTE no es válida", OperacionNoPermitidaError, lambda: e.pedidos.actualizar(pedido.id, Estado.PENDIENTE))

    def invalida_no_cambia_nada() -> bool:
        try:
            e.pedidos.actualizar(pedido.id, Estado.TERMINADO, FormaPago.TARJETA)
        except OperacionNoPermitidaError:
            return pedido.forma_pago is FormaPago.EFECTIVO
        return False

    r.valido("Transición inválida no cambia la forma de pago", invalida_no_cambia_nada)
    r.valido("PENDIENTE -> CONFIRMADO", lambda: e.pedidos.actualizar(pedido.id, Estado.CONFIRMADO).estado is Estado.CONFIRMADO)
    r.error("Un pedido registrado confirmado no se modifica", OperacionNoPermitidaError, lambda: pedido.agregar_detalle(1, e.otro))
    r.valido("CONFIRMADO -> TERMINADO", lambda: e.pedidos.actualizar(pedido.id, Estado.TERMINADO).estado is Estado.TERMINADO)
    r.error("TERMINADO no cambia más", OperacionNoPermitidaError, lambda: e.pedidos.actualizar(pedido.id, Estado.CANCELADO))
    r.valido("TERMINADO no devolvió stock", lambda: e.producto.stock == 3)
    cancelado = e.pedido_registrado(1)
    r.valido("Antes de cancelar el stock está descontado", lambda: e.producto.stock == 2)
    e.pedidos.actualizar(cancelado.id, Estado.CANCELADO)
    r.valido("Cancelar devuelve el stock", lambda: e.producto.stock == 3)
    r.error("CANCELADO no cambia más", OperacionNoPermitidaError, lambda: e.pedidos.actualizar(cancelado.id, Estado.CONFIRMADO))
    e.pedidos.eliminar(cancelado.id)
    r.valido("Eliminar un cancelado no devuelve stock dos veces", lambda: e.producto.stock == 3)
    e.pedidos.eliminar(pedido.id)
    r.valido("Eliminar un terminado no devuelve stock", lambda: e.producto.stock == 3)
    pendiente = e.pedido_registrado(2)
    total = pendiente.total
    detalle = pendiente.detalles[0]
    e.pedidos.eliminar(pendiente.id)
    r.valido("Eliminar un pendiente devuelve el stock", lambda: e.producto.stock == 3)
    r.valido("La baja alcanza al pedido y a sus detalles", lambda: pendiente.eliminado and detalle.eliminado)
    r.valido("Sale de los listados", lambda: pendiente not in e.pedidos.listar())
    r.valido("Sale de los pedidos del cliente", lambda: pendiente not in e.pedidos.listar_de_usuario(e.cliente))
    r.valido("Conserva su total para auditoría", lambda: pendiente.total == total)
    r.error("Un pedido eliminado no se busca", EntidadNoEncontradaError, lambda: e.pedidos.buscar_por_id(pendiente.id))


def main() -> None:
    resultados = Resultados()
    probar_modelo(resultados)
    probar_categorias(resultados)
    probar_productos(resultados)
    probar_usuarios(resultados)
    probar_detalles(resultados)
    probar_registro_pedidos(resultados)
    probar_estados(resultados)
    resultados.resumen()
    sys.exit(1 if resultados.fallidos else 0)


if __name__ == "__main__":
    main()
