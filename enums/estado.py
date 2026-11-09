"""Estados de un pedido y sus transiciones válidas."""
from enum import Enum


class Estado(Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADO = "CONFIRMADO"
    TERMINADO = "TERMINADO"
    CANCELADO = "CANCELADO"

    def puede_pasar_a(self, nuevo: "Estado") -> bool:
        """Indica si la transición desde este estado hacia `nuevo` es válida."""
        transiciones: dict[Estado, tuple[Estado, ...]] = {
            Estado.PENDIENTE: (Estado.CONFIRMADO, Estado.CANCELADO),
            Estado.CONFIRMADO: (Estado.TERMINADO, Estado.CANCELADO),
        }
        return nuevo in transiciones.get(self, ())
