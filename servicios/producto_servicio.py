"""Servicio de productos."""
from entidades import Producto
from servicios.categoria_servicio import CategoriaServicio
from servicios.servicio_base import ServicioBase


class ProductoServicio(ServicioBase[Producto]):
    _nombre_entidad = "el producto"

    def __init__(self, categorias: CategoriaServicio) -> None:
        super().__init__()
        self.__categorias: CategoriaServicio = categorias

    def crear(
        self,
        nombre: str,
        precio: float,
        stock: int,
        categoria_id: int,
        descripcion: str = "",
        imagen: str = "",
        disponible: bool = True,
    ) -> Producto:
        categoria = self.__categorias.buscar_por_id(categoria_id)
        producto = Producto(nombre, precio, stock, categoria, descripcion, imagen, disponible)
        self._agregar(producto)
        return producto

    def editar(
        self,
        producto_id: int,
        nombre: str | None = None,
        precio: float | None = None,
        stock: int | None = None,
        categoria_id: int | None = None,
        descripcion: str | None = None,
        imagen: str | None = None,
        disponible: bool | None = None,
    ) -> Producto:
        producto = self.buscar_por_id(producto_id)
        categoria = None
        if categoria_id is not None:
            categoria = self.__categorias.buscar_por_id(categoria_id)
        self._aplicar_cambios(
            producto,
            {
                "nombre": nombre,
                "precio": precio,
                "stock": stock,
                "categoria": categoria,
                "descripcion": descripcion,
                "imagen": imagen,
                "disponible": disponible,
            },
        )
        return producto

    def eliminar(self, producto_id: int) -> None:
        self.buscar_por_id(producto_id).eliminar()

    def listar_disponibles(self) -> list[Producto]:
        """Catálogo del cliente: disponibles y con stock."""
        return [p for p in self.listar() if p.disponible and p.stock > 0]

    def listar_por_categoria(self, categoria_id: int) -> list[Producto]:
        categoria = self.__categorias.buscar_por_id(categoria_id)
        return list(categoria.productos_activos)
