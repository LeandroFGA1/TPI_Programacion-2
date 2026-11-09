"""Clase abstracta Menu y mecánica común de los menús."""
from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence

from consola.lectura import leer_texto
from entidades import Base, Pedido, Usuario
from excepciones import FoodStoreError

type Accion = Callable[[], None]
type Opciones = dict[str, tuple[str, Accion]]


class Menu(ABC):
    """Cada rol tiene su subclase; el programa solo llama a mostrar()."""

    def __init__(self, usuario: Usuario) -> None:
        self._usuario: Usuario = usuario

    @abstractmethod
    def mostrar(self) -> bool:
        """Devuelve True para cerrar sesión y False para salir del programa."""

    def _correr_principal(self, titulo: str, opciones: Opciones) -> bool:
        while True:
            self._imprimir_opciones(titulo, opciones)
            print("9. Cerrar sesión")
            print("0. Salir")
            seleccion = leer_texto("Seleccione: ")
            if seleccion == "9":
                return True
            if seleccion == "0":
                return False
            self._ejecutar(opciones, seleccion)

    def _correr_submenu(self, titulo: str, opciones: Opciones) -> None:
        while True:
            self._imprimir_opciones(titulo, opciones)
            print("0. Volver")
            seleccion = leer_texto("Seleccione: ")
            if seleccion == "0":
                return
            self._ejecutar(opciones, seleccion)

    @staticmethod
    def _imprimir_opciones(titulo: str, opciones: Opciones) -> None:
        print(f"\n{titulo}")
        for clave, (descripcion, _) in opciones.items():
            print(f"{clave}. {descripcion}")

    def _ejecutar(self, opciones: Opciones, seleccion: str) -> None:
        """Corre la acción elegida: ningún error llega a cerrar el programa."""
        if seleccion not in opciones:
            self._informar_error("Opción inválida.")
            return
        try:
            opciones[seleccion][1]()
        except FoodStoreError as error:
            self._informar_error(str(error))
        except ValueError:
            self._informar_error("Debe ingresar un número válido.")

    @staticmethod
    def _informar_exito(mensaje: str) -> None:
        print(f"[OK] {mensaje}")

    @staticmethod
    def _informar_error(mensaje: str) -> None:
        print(f"[ERROR] {mensaje}")

    @staticmethod
    def _mostrar_lista(elementos: Sequence[Base], mensaje_vacio: str) -> None:
        if not elementos:
            print(mensaje_vacio)
        for elemento in elementos:
            print(elemento)

    @staticmethod
    def _mostrar_detalle_pedido(pedido: Pedido) -> None:
        print(pedido)
        for detalle in pedido.detalles:
            print(f"   - {detalle}")
        print(f"   TOTAL: ${pedido.total:.2f}")
