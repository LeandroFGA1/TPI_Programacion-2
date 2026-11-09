# Food Store – Sistema de gestión de pedidos por consola

Trabajo Práctico Integrador de **Programación II** (Tecnicatura Universitaria en Programación a Distancia, UTN).
Aplicación de consola en Python con Programación Orientada a Objetos. Toda la información vive en memoria mientras el programa se ejecuta.

## Cómo ejecutar

Requiere **Python 3.12 o superior**. No necesita instalar dependencias: usa solo la biblioteca estándar.

```bash
cd food_store         # omitir si ya se esta dentro de la carpeta o la version del repo
python main.py        # inicia el sistema
python pruebas.py     # muestra los casos válidos y los errores esperados
```

En algunos sistemas el comando es `python3` (Linux/macOS) o `py` (Windows).

## Credenciales

| Rol | Mail | Contraseña |
|---|---|---|
| ADMIN (administrador inicial) | `admin@foodstore.com` | `admin123` |
| USUARIO (cliente de ejemplo) | `juan@foodstore.com` | `juan123` |

La contraseña no se muestra mientras se escribe.

## Estructura

```
food_store/
├── main.py          # crea los servicios y arranca los menús
├── pruebas.py       # pruebas del modelo y los servicios, sin menú
├── entidades/       # clases del UML y la interfaz Calculable
├── enums/           # Rol, Estado, FormaPago
├── excepciones/     # FoodStoreError y sus subclases
├── servicios/       # un servicio por entidad con su colección
└── consola/         # Menu, MenuAdministrador, MenuCliente, inicio de sesión y lectura validada
```

La dependencia va en un solo sentido: consola → servicios → entidades.

## Entrega

- **Informe:** [Informe_TPI_FoodStore.pdf](Informe_TPI_FoodStore.pdf) (en la raíz del proyecto)
- **Video demostración:** Pegar aca el video, no olvidar. V
