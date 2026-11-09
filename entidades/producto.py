"""Entidad Producto."""
from entidades.base import Base
from entidades.categoria import Categoria
from excepciones import (
    DatoInvalidoError,
    EntidadNoEncontradaError,
    PrecioInvalidoError,
    StockInvalidoError,
)


class Producto(Base):
    """Artículo del catálogo, asociado a una categoría (N..1)."""

    __nombre: str
    __precio: float
    __stock: int
    __descripcion: str
    __imagen: str
    __disponible: bool

    def __init__(
        self,
        nombre: str,
        precio: float,
        stock: int,
        categoria: Categoria,
        descripcion: str = "",
        imagen: str = "",
        disponible: bool = True,
    ) -> None:
        super().__init__()
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.descripcion = descripcion
        self.imagen = imagen
        self.disponible = disponible
        self.__categoria: Categoria = self.__validar_categoria(categoria)
        categoria.agregar_producto(self)

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = self._validar_texto(valor, "El nombre del producto")

    @property
    def precio(self) -> float:
        return self.__precio

    @precio.setter
    def precio(self, valor: float) -> None:
        # La comparación encadenada también rechaza NaN e infinito.
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise PrecioInvalidoError("El precio debe ser un número.")
        if not 0 <= valor < float("inf"):
            raise PrecioInvalidoError("El precio debe ser un número mayor o igual a 0.")
        self.__precio = float(valor)

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise StockInvalidoError("El stock debe ser un número entero.")
        if valor < 0:
            raise StockInvalidoError("El stock no puede ser negativo.")
        self.__stock = valor

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        self.__descripcion = self.__validar_texto_libre(valor, "La descripción")

    @property
    def imagen(self) -> str:
        return self.__imagen

    @imagen.setter
    def imagen(self, valor: str) -> None:
        self.__imagen = self.__validar_texto_libre(valor, "La imagen")

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise DatoInvalidoError("La disponibilidad debe ser verdadero o falso.")
        self.__disponible = valor

    @property
    def categoria(self) -> Categoria:
        return self.__categoria

    @categoria.setter
    def categoria(self, valor: Categoria) -> None:
        nueva = self.__validar_categoria(valor)
        self.__categoria.quitar_producto(self)
        self.__categoria = nueva
        nueva.agregar_producto(self)

    @staticmethod
    def __validar_categoria(valor: Categoria) -> Categoria:
        if not isinstance(valor, Categoria) or valor.eliminado:
            raise EntidadNoEncontradaError("La categoría no existe o está eliminada.")
        return valor

    @staticmethod
    def __validar_texto_libre(valor: str, campo: str) -> str:
        if not isinstance(valor, str):
            raise DatoInvalidoError(f"{campo} debe ser un texto.")
        return valor.strip()

    def __str__(self) -> str:
        disponible = "Sí" if self.disponible else "No"
        return (
            f"[{self.id}] {self.nombre} | ${self.precio:.2f} | Stock: {self.stock} "
            f"| Categoría: {self.categoria.nombre} | Disponible: {disponible}"
        )
