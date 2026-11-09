"""Entidad Categoria."""
from __future__ import annotations

from typing import TYPE_CHECKING

from entidades.base import Base

if TYPE_CHECKING:
    from entidades.producto import Producto


class Categoria(Base):
    """Agrupa productos (agregación 1..N: el producto existe por sí mismo)."""

    __nombre: str
    __descripcion: str

    def __init__(self, nombre: str, descripcion: str) -> None:
        super().__init__()
        self.nombre = nombre
        self.descripcion = descripcion
        self.__productos: list[Producto] = []

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = self._validar_texto(valor, "El nombre de la categoría")

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        self.__descripcion = self._validar_texto(valor, "La descripción de la categoría")

    @property
    def productos(self) -> tuple[Producto, ...]:
        """Copia inmutable de todos los productos asociados."""
        return tuple(self.__productos)

    @property
    def productos_activos(self) -> tuple[Producto, ...]:
        """Productos asociados que no fueron dados de baja."""
        return tuple(p for p in self.__productos if not p.eliminado)

    def agregar_producto(self, producto: Producto) -> None:
        """Asocia un producto a la categoría."""
        if producto not in self.__productos:
            self.__productos.append(producto)

    def quitar_producto(self, producto: Producto) -> None:
        """Desasocia un producto de la categoría."""
        if producto in self.__productos:
            self.__productos.remove(producto)

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} | {self.descripcion}"
