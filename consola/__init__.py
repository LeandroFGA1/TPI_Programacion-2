"""Interfaz de consola: menús, inicio de sesión y lectura de datos."""
from consola.fabrica_menu import crear_menu
from consola.inicio_sesion import iniciar_sesion
from consola.menu import Menu
from consola.menu_administrador import MenuAdministrador
from consola.menu_cliente import MenuCliente

__all__ = ["Menu", "MenuAdministrador", "MenuCliente", "crear_menu", "iniciar_sesion"]
