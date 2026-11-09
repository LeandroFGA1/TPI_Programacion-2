"""Servicio de categorías."""
from entidades import Categoria
from excepciones import DuplicadoError, OperacionNoPermitidaError
from servicios.servicio_base import ServicioBase


class CategoriaServicio(ServicioBase[Categoria]):
    _nombre_entidad = "la categoría"

    def crear(self, nombre: str, descripcion: str) -> Categoria:
        self.__validar_nombre_unico(nombre)
        categoria = Categoria(nombre, descripcion)
        self._agregar(categoria)
        return categoria

    def editar(
        self,
        categoria_id: int,
        nombre: str | None = None,
        descripcion: str | None = None,
    ) -> Categoria:
        categoria = self.buscar_por_id(categoria_id)
        if nombre is not None:
            self.__validar_nombre_unico(nombre, categoria)
        self._aplicar_cambios(categoria, {"nombre": nombre, "descripcion": descripcion})
        return categoria

    def eliminar(self, categoria_id: int) -> None:
        categoria = self.buscar_por_id(categoria_id)
        activos = len(categoria.productos_activos)
        if activos > 0:
            raise OperacionNoPermitidaError(
                f"No se puede eliminar: la categoría tiene {activos} producto(s) activo(s)."
            )
        categoria.eliminar()

    def __validar_nombre_unico(self, nombre: str, propia: Categoria | None = None) -> None:
        buscado = nombre.strip().casefold()
        for categoria in self._todos():
            if categoria != propia and categoria.nombre.casefold() == buscado:
                estado = " (dada de baja)" if categoria.eliminado else ""
                raise DuplicadoError(f"Ya existe una categoría con ese nombre{estado}.")
