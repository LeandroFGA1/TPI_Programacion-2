"""Pantalla de inicio de sesión."""
from consola.lectura import leer_contrasenia, leer_texto
from entidades import Usuario
from excepciones import CredencialesInvalidasError
from servicios import UsuarioServicio


def iniciar_sesion(usuarios: UsuarioServicio, intentos: int = 3) -> Usuario | None:
    """Devuelve el usuario autenticado o None si se agotan los intentos."""
    for i in range(intentos):
        print("\nFOOD STORE – INICIO DE SESIÓN")
        correo = leer_texto("Correo: ")
        contrasenia = leer_contrasenia("Contraseña: ")
        try:
            usuario = usuarios.autenticar(correo, contrasenia)
        except CredencialesInvalidasError as error:
            print(error)
        else:
            print(f"\nBienvenido, {usuario.nombre_completo} {usuario.rol.value}")
            return usuario
    print("Se agotaron los intentos. El programa se cerrará.")
    return None
