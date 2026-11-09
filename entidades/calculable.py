"""Interfaz Calculable."""
from abc import ABC, abstractmethod


class Calculable(ABC):
    """Contrato para los objetos que calculan un total."""

    @abstractmethod
    def calcular_total(self) -> None:
        """Actualiza el total del objeto que implementa la interfaz."""
