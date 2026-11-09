"""Menú del rol USUARIO: solo consulta."""
from consola.lectura import leer_entero_opcional
from consola.menu import Menu, Opciones
from entidades import Usuario
from servicios import CategoriaServicio, PedidoServicio, ProductoServicio


class MenuCliente(Menu):
    def __init__(
        self,
        usuario: Usuario,
        categorias: CategoriaServicio,
        productos: ProductoServicio,
        pedidos: PedidoServicio,
    ) -> None:
        super().__init__(usuario)
        self.__categorias: CategoriaServicio = categorias
        self.__productos: ProductoServicio = productos
        self.__pedidos: PedidoServicio = pedidos

    def mostrar(self) -> bool:
        titulo = f"=== FOOD STORE – CLIENTE ({self._usuario.nombre_completo}) ==="
        opciones: Opciones = {
            "1": ("Ver categorías", self.__ver_categorias),
            "2": ("Ver productos disponibles", self.__ver_productos),
            "3": ("Mis pedidos", self.__ver_mis_pedidos),
            "4": ("Mis datos", self.__ver_mis_datos),
        }
        return self._correr_principal(titulo, opciones)

    def __ver_categorias(self) -> None:
        self._mostrar_lista(self.__categorias.listar(), "No hay categorías cargadas.")

    def __ver_productos(self) -> None:
        self._mostrar_lista(self.__productos.listar_disponibles(), "No hay productos disponibles.")

    def __ver_mis_pedidos(self) -> None:
        pedidos = self.__pedidos.listar_de_usuario(self._usuario)
        self._mostrar_lista(pedidos, "No tiene pedidos registrados.")
        if pedidos:
            pedido_id = leer_entero_opcional("Id para ver el detalle (Enter vuelve): ")
            if pedido_id is not None:
                pedido = self.__pedidos.buscar_de_usuario(pedido_id, self._usuario)
                self._mostrar_detalle_pedido(pedido)

    def __ver_mis_datos(self) -> None:
        print(f"Nombre:   {self._usuario.nombre}")
        print(f"Apellido: {self._usuario.apellido}")
        print(f"Mail:     {self._usuario.mail}")
        print(f"Celular:  {self._usuario.celular}")
        print(f"Rol:      {self._usuario.rol.value}")
