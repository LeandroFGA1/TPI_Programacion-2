"""Entidad Usuario."""
from __future__ import annotations

from typing import TYPE_CHECKING

from entidades.base import Base
from enums import Rol
from excepciones import DatoInvalidoError

if TYPE_CHECKING:
    from entidades.pedido import Pedido


class Usuario(Base):
    """Persona que usa el sistema; se asocia con sus pedidos (1..N)."""

    __nombre: str
    __apellido: str
    __mail: str
    __celular: str
    __contrasenia: str
    __rol: Rol

    def __init__(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> None:
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        self.cambiar_contrasenia(contrasenia)
        self.rol = rol
        self.__pedidos: list[Pedido] = []

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = self._validar_texto(valor, "El nombre")

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        self.__apellido = self._validar_texto(valor, "El apellido")

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

    @property
    def mail(self) -> str:
        return self.__mail

    @mail.setter
    def mail(self, valor: str) -> None:
        mail = self._validar_texto(valor, "El mail").lower()
        if "@" not in mail or "." not in mail or " " in mail:
            raise DatoInvalidoError("El mail debe tener un formato válido (contener '@' y '.').")
        self.__mail = mail

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, valor: str) -> None:
        self.__celular = self._validar_texto(valor, "El celular")

    @property
    def rol(self) -> Rol:
        return self.__rol

    @rol.setter
    def rol(self, valor: Rol) -> None:
        if not isinstance(valor, Rol):
            raise DatoInvalidoError("El rol no es válido.")
        self.__rol = valor

    @property
    def pedidos(self) -> tuple[Pedido, ...]:
        """Copia inmutable de los pedidos del usuario."""
        return tuple(self.__pedidos)

    def agregar_pedido(self, pedido: Pedido) -> None:
        """Asocia un pedido ya registrado al usuario."""
        if pedido not in self.__pedidos:
            self.__pedidos.append(pedido)

    def verificar_contrasenia(self, contrasenia: str) -> bool:
        """Compara sin exponer nunca la contraseña almacenada."""
        return self.__contrasenia == contrasenia

    def cambiar_contrasenia(self, contrasenia: str) -> None:
        """Reemplaza la contraseña, previa validación."""
        self.__contrasenia = self.validar_contrasenia(contrasenia)

    @staticmethod
    def validar_contrasenia(contrasenia: str) -> str:
        """Devuelve la contraseña si es válida o lanza DatoInvalidoError."""
        if not isinstance(contrasenia, str) or not contrasenia.strip():
            raise DatoInvalidoError("La contraseña no puede estar vacía.")
        return contrasenia

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} {self.apellido} | {self.mail} | {self.rol.value}"
