"""Clase abstracta de la que heredan todas las entidades."""
from abc import ABC, abstractmethod
from datetime import datetime

from excepciones import DatoInvalidoError


class Base(ABC):
    """Aporta id automático, baja lógica, fecha de creación e igualdad por id."""

    __contador: int = 0

    def __init__(self) -> None:
        Base.__contador += 1
        self.__id: int = Base.__contador
        self.__eliminado: bool = False
        self.__creado_en: datetime = datetime.now()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def eliminado(self) -> bool:
        return self.__eliminado

    @property
    def creado_en(self) -> datetime:
        return self.__creado_en

    def eliminar(self) -> None:
        """Realiza la baja lógica: el objeto sigue en su colección."""
        self.__eliminado = True

    @abstractmethod
    def __str__(self) -> str:
        """Devuelve una línea útil para los listados de consola."""

    def __eq__(self, otro: object) -> bool:
        return isinstance(otro, Base) and self.__id == otro.id

    def __hash__(self) -> int:
        return hash(self.__id)

    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        """Devuelve el texto sin espacios externos o falla si está vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError(f"{campo} no puede estar vacío.")
        return valor.strip()
