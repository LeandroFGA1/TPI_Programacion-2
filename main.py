"""Punto de entrada de Food Store: crea los servicios y arranca los menús."""
from consola import crear_menu, iniciar_sesion
from enums import Estado, FormaPago, Rol
from servicios import (
    CategoriaServicio,
    PedidoServicio,
    ProductoServicio,
    UsuarioServicio,
)


def cargar_datos_iniciales(
    categorias: CategoriaServicio,
    productos: ProductoServicio,
    usuarios: UsuarioServicio,
    pedidos: PedidoServicio,
) -> None:
    """Carga el administrador inicial y datos de ejemplo."""
    usuarios.crear("Ana", "Pérez", "admin@foodstore.com", "1155550001", "admin123", Rol.ADMIN)
    juan = usuarios.crear(
        "Juan", "Gómez", "juan@foodstore.com", "1155550002", "juan123", Rol.USUARIO
    )
    pizzas = categorias.crear("Pizzas", "Pizzas a la piedra")
    bebidas = categorias.crear("Bebidas", "Gaseosas y aguas")
    categorias.crear("Postres", "Postres caseros")
    muzzarella = productos.crear("Pizza muzzarella", 9500.0, 10, pizzas.id, "Clásica", "muzza.jpg")
    productos.crear("Pizza napolitana", 11000.0, 2, pizzas.id, "Con tomate y ajo", "napo.jpg")
    gaseosa = productos.crear("Gaseosa 1.5 L", 3200.0, 24, bebidas.id, "Línea cola", "cola.jpg")
    productos.crear("Agua saborizada", 2500.0, 8, bebidas.id, "Pomelo", "agua.jpg", False)
    pedido = pedidos.iniciar(juan.id, FormaPago.EFECTIVO)
    pedidos.agregar_detalle(pedido, muzzarella.id, 1)
    pedidos.agregar_detalle(pedido, gaseosa.id, 2)
    pedidos.registrar(pedido)
    pedidos.actualizar(pedido.id, Estado.CONFIRMADO)


def ejecutar_sesiones(
    categorias: CategoriaServicio,
    productos: ProductoServicio,
    usuarios: UsuarioServicio,
    pedidos: PedidoServicio,
) -> None:
    """Repite inicio de sesión y menú hasta salir o agotar los intentos."""
    while True:
        usuario = iniciar_sesion(usuarios)
        if usuario is None:
            return
        menu = crear_menu(usuario, categorias, productos, usuarios, pedidos)
        if not menu.mostrar():
            print("Hasta luego.")
            return


def main() -> None:
    categorias = CategoriaServicio()
    productos = ProductoServicio(categorias)
    usuarios = UsuarioServicio()
    pedidos = PedidoServicio(usuarios, productos)
    cargar_datos_iniciales(categorias, productos, usuarios, pedidos)
    try:
        ejecutar_sesiones(categorias, productos, usuarios, pedidos)
    except (EOFError, KeyboardInterrupt):
        print("\nEntrada interrumpida. El programa se cerrará.")


if __name__ == "__main__":
    main()
