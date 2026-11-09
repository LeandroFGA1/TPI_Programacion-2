"""Menú del rol ADMIN: gestión completa."""
from consola.lectura import (
    elegir_enum,
    elegir_enum_opcional,
    leer_contrasenia,
    leer_decimal,
    leer_decimal_opcional,
    leer_entero,
    leer_entero_opcional,
    leer_obligatorio,
    leer_opcional,
    leer_si_no,
    leer_si_no_opcional,
    leer_texto,
)
from consola.menu import Menu, Opciones
from entidades import Pedido, Usuario
from enums import Estado, FormaPago, Rol
from excepciones import DuplicadoError, FoodStoreError
from servicios import (
    CategoriaServicio,
    PedidoServicio,
    ProductoServicio,
    UsuarioServicio,
)


class MenuAdministrador(Menu):
    def __init__(
        self,
        usuario: Usuario,
        categorias: CategoriaServicio,
        productos: ProductoServicio,
        usuarios: UsuarioServicio,
        pedidos: PedidoServicio,
    ) -> None:
        super().__init__(usuario)
        self.__categorias: CategoriaServicio = categorias
        self.__productos: ProductoServicio = productos
        self.__usuarios: UsuarioServicio = usuarios
        self.__pedidos: PedidoServicio = pedidos

    def mostrar(self) -> bool:
        titulo = f"=== FOOD STORE – ADMINISTRADOR ({self._usuario.nombre_completo}) ==="
        opciones: Opciones = {
            "1": ("Categorías", self.__menu_categorias),
            "2": ("Productos", self.__menu_productos),
            "3": ("Usuarios", self.__menu_usuarios),
            "4": ("Pedidos", self.__menu_pedidos),
        }
        return self._correr_principal(titulo, opciones)

    # ----- Categorías -----

    def __menu_categorias(self) -> None:
        opciones: Opciones = {
            "1": ("Listar", self.__listar_categorias),
            "2": ("Crear", self.__crear_categoria),
            "3": ("Editar", self.__editar_categoria),
            "4": ("Eliminar", self.__eliminar_categoria),
        }
        self._correr_submenu("--- CATEGORÍAS ---", opciones)

    def __listar_categorias(self) -> None:
        self._mostrar_lista(self.__categorias.listar(), "No hay categorías cargadas.")

    def __crear_categoria(self) -> None:
        nombre = leer_obligatorio("Nombre: ")
        descripcion = leer_obligatorio("Descripción: ")
        categoria = self.__categorias.crear(nombre, descripcion)
        self._informar_exito(f"Categoría creada con id {categoria.id}.")

    def __editar_categoria(self) -> None:
        self.__listar_categorias()
        categoria = self.__categorias.buscar_por_id(leer_entero("Id de la categoría: "))
        nombre = leer_opcional(f"Nombre [{categoria.nombre}]: ")
        descripcion = leer_opcional(f"Descripción [{categoria.descripcion}]: ")
        self.__categorias.editar(categoria.id, nombre, descripcion)
        self._informar_exito("Categoría actualizada.")

    def __eliminar_categoria(self) -> None:
        self.__listar_categorias()
        categoria_id = leer_entero("Id de la categoría: ")
        self.__categorias.buscar_por_id(categoria_id)
        if self.__confirmar():
            self.__categorias.eliminar(categoria_id)
            self._informar_exito("Categoría eliminada.")

    # ----- Productos -----

    def __menu_productos(self) -> None:
        opciones: Opciones = {
            "1": ("Listar", self.__listar_productos),
            "2": ("Crear", self.__crear_producto),
            "3": ("Editar", self.__editar_producto),
            "4": ("Eliminar", self.__eliminar_producto),
            "5": ("Listar por categoría", self.__listar_productos_por_categoria),
        }
        self._correr_submenu("--- PRODUCTOS ---", opciones)

    def __listar_productos(self) -> None:
        self._mostrar_lista(self.__productos.listar(), "No hay productos cargados.")

    def __listar_productos_por_categoria(self) -> None:
        self.__listar_categorias()
        productos = self.__productos.listar_por_categoria(leer_entero("Id de la categoría: "))
        self._mostrar_lista(productos, "La categoría no tiene productos.")

    def __crear_producto(self) -> None:
        nombre = leer_obligatorio("Nombre: ")
        descripcion = leer_texto("Descripción: ")
        precio = leer_decimal("Precio: ")
        stock = leer_entero("Stock: ")
        imagen = leer_texto("Imagen (URL o archivo): ")
        disponible = leer_si_no("¿Disponible?")
        self.__listar_categorias()
        categoria_id = leer_entero("Id de la categoría: ")
        producto = self.__productos.crear(
            nombre, precio, stock, categoria_id, descripcion, imagen, disponible
        )
        self._informar_exito(f"Producto creado con id {producto.id}.")

    def __editar_producto(self) -> None:
        self.__listar_productos()
        producto = self.__productos.buscar_por_id(leer_entero("Id del producto: "))
        print("Presione Enter para conservar el valor actual.")
        nombre = leer_opcional(f"Nombre [{producto.nombre}]: ")
        descripcion = leer_opcional(f"Descripción [{producto.descripcion}]: ")
        precio = leer_decimal_opcional(f"Precio [{producto.precio:.2f}]: ")
        stock = leer_entero_opcional(f"Stock [{producto.stock}]: ")
        imagen = leer_opcional(f"Imagen [{producto.imagen}]: ")
        disponible = leer_si_no_opcional("¿Disponible?")
        self.__listar_categorias()
        categoria_id = leer_entero_opcional(f"Id de la categoría [{producto.categoria.id}]: ")
        self.__productos.editar(
            producto.id, nombre, precio, stock, categoria_id, descripcion, imagen, disponible
        )
        self._informar_exito("Producto actualizado.")

    def __eliminar_producto(self) -> None:
        self.__listar_productos()
        producto = self.__productos.buscar_por_id(leer_entero("Id del producto: "))
        if self.__confirmar():
            self.__productos.eliminar(producto.id)
            self._informar_exito("Producto eliminado.")

    # ----- Usuarios -----

    def __menu_usuarios(self) -> None:
        opciones: Opciones = {
            "1": ("Listar", self.__listar_usuarios),
            "2": ("Crear", self.__crear_usuario),
            "3": ("Editar", self.__editar_usuario),
            "4": ("Eliminar", self.__eliminar_usuario),
        }
        self._correr_submenu("--- USUARIOS ---", opciones)

    def __listar_usuarios(self) -> None:
        self._mostrar_lista(self.__usuarios.listar(), "No hay usuarios cargados.")

    def __crear_usuario(self) -> None:
        nombre = leer_obligatorio("Nombre: ")
        apellido = leer_obligatorio("Apellido: ")
        mail = self.__leer_mail_disponible()
        celular = leer_obligatorio("Celular: ")
        contrasenia = leer_contrasenia("Contraseña: ")
        rol = elegir_enum("Rol:", Rol)
        usuario = self.__usuarios.crear(nombre, apellido, mail, celular, contrasenia, rol)
        self._informar_exito(f"Usuario creado con id {usuario.id}.")

    def __leer_mail_disponible(self) -> str:
        """Si el mail ya existe, informa y pide otro; vacío vuelve al menú."""
        while True:
            mail = leer_obligatorio("Mail: ")
            try:
                self.__usuarios.validar_mail_disponible(mail)
            except DuplicadoError as error:
                self._informar_error(f"{error} Ingrese otro.")
            else:
                return mail

    def __editar_usuario(self) -> None:
        self.__listar_usuarios()
        usuario = self.__usuarios.buscar_por_id(leer_entero("Id del usuario: "))
        print("Presione Enter para conservar el valor actual.")
        nombre = leer_opcional(f"Nombre [{usuario.nombre}]: ")
        apellido = leer_opcional(f"Apellido [{usuario.apellido}]: ")
        mail = leer_opcional(f"Mail [{usuario.mail}]: ")
        celular = leer_opcional(f"Celular [{usuario.celular}]: ")
        contrasenia = leer_contrasenia("Nueva contraseña (Enter conserva): ") or None
        rol = elegir_enum_opcional(f"Rol [{usuario.rol.name}]:", Rol)
        self.__usuarios.editar(
            usuario.id, self._usuario, nombre, apellido, mail, celular, contrasenia, rol
        )
        self._informar_exito("Usuario actualizado.")

    def __eliminar_usuario(self) -> None:
        self.__listar_usuarios()
        usuario = self.__usuarios.buscar_por_id(leer_entero("Id del usuario: "))
        if self.__confirmar():
            self.__usuarios.eliminar(usuario.id, self._usuario)
            self._informar_exito("Usuario eliminado.")

    # ----- Pedidos -----

    def __menu_pedidos(self) -> None:
        opciones: Opciones = {
            "1": ("Listar", self.__listar_pedidos),
            "2": ("Crear", self.__crear_pedido),
            "3": ("Actualizar estado / forma de pago", self.__actualizar_pedido),
            "4": ("Eliminar", self.__eliminar_pedido),
            "5": ("Ver detalles de un pedido", self.__ver_detalle_pedido),
            "6": ("Listar por usuario", self.__listar_pedidos_por_usuario),
        }
        self._correr_submenu("--- PEDIDOS ---", opciones)

    def __listar_pedidos(self) -> None:
        self._mostrar_lista(self.__pedidos.listar(), "No hay pedidos cargados.")

    def __listar_pedidos_por_usuario(self) -> None:
        self.__listar_usuarios()
        usuario = self.__usuarios.buscar_por_id(leer_entero("Id del usuario: "))
        pedidos = self.__pedidos.listar_de_usuario(usuario)
        self._mostrar_lista(pedidos, "El usuario no tiene pedidos.")

    def __ver_detalle_pedido(self) -> None:
        self.__listar_pedidos()
        self._mostrar_detalle_pedido(self.__pedidos.buscar_por_id(leer_entero("Id del pedido: ")))

    def __crear_pedido(self) -> None:
        self.__listar_usuarios()
        usuario_id = leer_entero("Id del usuario: ")
        forma_pago = elegir_enum("Forma de pago:", FormaPago)
        pedido = self.__pedidos.iniciar(usuario_id, forma_pago)
        try:
            if not self.__cargar_detalles(pedido):
                self._informar_error("Creación cancelada por el operador.")
                return
            self.__pedidos.registrar(pedido)
        except FoodStoreError as error:
            self.__informar_creacion_cancelada(str(error))
        except ValueError:
            self.__informar_creacion_cancelada("Debe ingresar un número válido.")
        else:
            self._informar_exito(f"Pedido creado con id {pedido.id}. Total: ${pedido.total:.2f}")

    def __informar_creacion_cancelada(self, motivo: str) -> None:
        self._informar_error(f"{motivo} Pedido cancelado: no se guardó ni cambió el stock.")

    def __cargar_detalles(self, pedido: Pedido) -> bool:
        """Devuelve True al confirmar y False si el operador cancela."""
        while True:
            print(f"\nDetalles cargados: {len(pedido.detalles)} | Total: ${pedido.total:.2f}")
            print("1. Agregar producto\n2. Quitar producto\n3. Confirmar pedido\n0. Cancelar")
            seleccion = leer_texto("Seleccione: ")
            if seleccion == "1":
                self.__agregar_producto_al_pedido(pedido)
            elif seleccion == "2":
                self.__quitar_producto_del_pedido(pedido)
            elif seleccion == "3":
                return True
            elif seleccion == "0":
                return False
            else:
                self._informar_error("Opción inválida.")

    def __agregar_producto_al_pedido(self, pedido: Pedido) -> None:
        self._mostrar_lista(self.__productos.listar_disponibles(), "No hay productos disponibles.")
        producto_id = leer_entero("Id del producto: ")
        cantidad = leer_entero("Cantidad: ")
        self.__pedidos.agregar_detalle(pedido, producto_id, cantidad)
        self._informar_exito("Producto agregado.")

    def __quitar_producto_del_pedido(self, pedido: Pedido) -> None:
        self._mostrar_detalle_pedido(pedido)
        self.__pedidos.quitar_detalle(pedido, leer_entero("Id del producto a quitar: "))
        self._informar_exito("Producto quitado.")

    def __actualizar_pedido(self) -> None:
        self.__listar_pedidos()
        pedido = self.__pedidos.buscar_por_id(leer_entero("Id del pedido: "))
        estado = elegir_enum_opcional(f"Estado [{pedido.estado.name}]:", Estado)
        forma_pago = elegir_enum_opcional(f"Forma de pago [{pedido.forma_pago.name}]:", FormaPago)
        self.__pedidos.actualizar(pedido.id, estado, forma_pago)
        self._informar_exito("Pedido actualizado.")

    def __eliminar_pedido(self) -> None:
        self.__listar_pedidos()
        pedido = self.__pedidos.buscar_por_id(leer_entero("Id del pedido: "))
        if self.__confirmar():
            self.__pedidos.eliminar(pedido.id)
            self._informar_exito("Pedido eliminado.")

    # ----- Auxiliares -----

    def __confirmar(self) -> bool:
        confirmado = leer_si_no("¿Confirma la operación?")
        if not confirmado:
            print("Operación cancelada.")
        return confirmado
