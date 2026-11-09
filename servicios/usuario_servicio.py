"""Servicio de usuarios."""
from entidades import Usuario
from enums import Rol
from excepciones import (
    CredencialesInvalidasError,
    DuplicadoError,
    OperacionNoPermitidaError,
)
from servicios.servicio_base import ServicioBase


class UsuarioServicio(ServicioBase[Usuario]):
    _nombre_entidad = "el usuario"

    def crear(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> Usuario:
        self.validar_mail_disponible(mail)
        usuario = Usuario(nombre, apellido, mail, celular, contrasenia, rol)
        self._agregar(usuario)
        return usuario

    def editar(
        self,
        usuario_id: int,
        actor: Usuario,
        nombre: str | None = None,
        apellido: str | None = None,
        mail: str | None = None,
        celular: str | None = None,
        contrasenia: str | None = None,
        rol: Rol | None = None,
    ) -> Usuario:
        usuario = self.buscar_por_id(usuario_id)
        if usuario == actor and rol is not None and rol is not usuario.rol:
            raise OperacionNoPermitidaError("No puede cambiar su propio rol.")
        if mail is not None:
            self.validar_mail_disponible(mail, usuario)
        if contrasenia is not None:
            Usuario.validar_contrasenia(contrasenia)
        self._aplicar_cambios(
            usuario,
            {
                "nombre": nombre,
                "apellido": apellido,
                "mail": mail,
                "celular": celular,
                "rol": rol,
            },
        )
        if contrasenia is not None:
            usuario.cambiar_contrasenia(contrasenia)
        return usuario

    def eliminar(self, usuario_id: int, actor: Usuario) -> None:
        usuario = self.buscar_por_id(usuario_id)
        if usuario == actor:
            raise OperacionNoPermitidaError("Un administrador no puede eliminarse a sí mismo.")
        usuario.eliminar()

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        """Devuelve el usuario activo o lanza un error sin revelar qué falló."""
        buscado = mail.strip().lower()
        for usuario in self.listar():
            if usuario.mail == buscado and usuario.verificar_contrasenia(contrasenia):
                return usuario
        raise CredencialesInvalidasError("Mail o contraseña incorrectos.")

    def validar_mail_disponible(self, mail: str, propio: Usuario | None = None) -> None:
        """Recorre la colección y lanza DuplicadoError si el mail ya está en uso."""
        buscado = mail.strip().lower()
        for usuario in self._todos():
            if usuario != propio and usuario.mail == buscado:
                estado = " (dado de baja)" if usuario.eliminado else ""
                raise DuplicadoError(f"Ya existe un usuario con ese mail{estado}.")
