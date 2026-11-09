# Funciones para pedirle datos al usuario por teclado.
# Si un numero esta mal escrito salta ValueError, y si un dato viene vacio
# o fuera de rango salta DatoInvalidoError. Los dos se atrapan en el menu.
from enum import Enum
from getpass import getpass

from excepciones import DatoInvalidoError


def leer_texto(mensaje: str) -> str:
    texto = input(mensaje)
    texto = texto.strip()
    return texto


def leer_obligatorio(mensaje: str) -> str:
    texto = leer_texto(mensaje)
    if texto == "":
        raise DatoInvalidoError("El dato no puede estar vacío.")
    return texto


# Se usa al editar: si el usuario aprieta Enter devuelve None
# y el servicio deja el valor que ya tenia.
def leer_opcional(mensaje: str) -> str | None:
    texto = leer_texto(mensaje)
    if texto == "":
        return None
    else:
        return texto


def leer_contrasenia(mensaje: str) -> str:
    contrasenia = getpass(mensaje)
    return contrasenia.strip()


def leer_entero(mensaje: str) -> int:
    texto = leer_texto(mensaje)
    numero = int(texto)
    return numero


def leer_entero_opcional(mensaje: str) -> int | None:
    texto = leer_texto(mensaje)
    if texto == "":
        return None
    else:
        return int(texto)


def leer_decimal(mensaje: str) -> float:
    texto = leer_texto(mensaje)
    # Aca se suele escribir 12,50 asi que acepto la coma tambien
    texto = texto.replace(",", ".")
    numero = float(texto)
    return numero


def leer_decimal_opcional(mensaje: str) -> float | None:
    texto = leer_texto(mensaje)
    if texto == "":
        return None
    else:
        texto = texto.replace(",", ".")
        return float(texto)


def _interpretar_si_no(texto: str) -> bool:
    respuesta = texto.upper()
    if respuesta == "S":
        return True
    elif respuesta == "N":
        return False
    else:
        raise DatoInvalidoError("Responda S o N.")


def leer_si_no(mensaje: str) -> bool:
    texto = leer_texto(mensaje + " (S/N): ")
    return _interpretar_si_no(texto)


def leer_si_no_opcional(mensaje: str) -> bool | None:
    texto = leer_texto(mensaje + " (S/N, Enter conserva): ")
    if texto == "":
        return None
    else:
        return _interpretar_si_no(texto)


# Muestra las opciones del enum con un numero al lado y devuelve la lista
def _mostrar_opciones_enum[E: Enum](titulo: str, enumerado: type[E]) -> list[E]:
    print(titulo)
    miembros = list(enumerado)
    numero = 1
    for miembro in miembros:
        print(f"  {numero}. {miembro.name}")
        numero = numero + 1
    return miembros


def _miembro_por_numero[E: Enum](miembros: list[E], numero: int) -> E:
    if numero < 1 or numero > len(miembros):
        raise DatoInvalidoError("Opción fuera de rango.")
    # Le resto 1 porque en pantalla empiezan en 1 y la lista en 0
    return miembros[numero - 1]


def elegir_enum[E: Enum](titulo: str, enumerado: type[E]) -> E:
    miembros = _mostrar_opciones_enum(titulo, enumerado)
    numero = leer_entero("Número: ")
    return _miembro_por_numero(miembros, numero)


# Igual que elegir_enum pero con Enter se queda con el valor actual
def elegir_enum_opcional[E: Enum](titulo: str, enumerado: type[E]) -> E | None:
    miembros = _mostrar_opciones_enum(titulo, enumerado)
    numero = leer_entero_opcional("Número (Enter conserva): ")
    if numero is None:
        return None
    else:
        return _miembro_por_numero(miembros, numero)