"""Comportamiento común de los servicios."""
from collections.abc import Mapping

from entidades import Base
from excepciones import EntidadNoEncontradaError, FoodStoreError


class ServicioBase[T: Base]:
    """Administra la colección en memoria de una entidad."""

    _nombre_entidad: str = "el elemento"

    def __init__(self) -> None:
        self.__elementos: list[T] = []

    def listar(self) -> list[T]:
        """Devuelve solo los elementos no eliminados."""
        return [e for e in self.__elementos if not e.eliminado]

    def buscar_por_id(self, id_buscado: int) -> T:
        """Devuelve el elemento activo con ese id o lanza una excepción."""
        for elemento in self.listar():
            if elemento.id == id_buscado:
                return elemento
        raise EntidadNoEncontradaError(
            f"No se encontró {self._nombre_entidad} con id {id_buscado}."
        )

    def _agregar(self, elemento: T) -> None:
        self.__elementos.append(elemento)

    def _todos(self) -> tuple[T, ...]:
        """Incluye los eliminados: la baja lógica no libera mail ni nombre."""
        return tuple(self.__elementos)

    @staticmethod
    def _aplicar_cambios(elemento: T, cambios: Mapping[str, object | None]) -> None:
        """Aplica los cambios no nulos: si uno falla, no se modifica nada."""
        efectivos = {campo: valor for campo, valor in cambios.items() if valor is not None}
        originales = {campo: getattr(elemento, campo) for campo in efectivos}
        try:
            for campo, valor in efectivos.items():
                setattr(elemento, campo, valor)
        except FoodStoreError:
            for campo, valor in originales.items():
                setattr(elemento, campo, valor)
            raise
