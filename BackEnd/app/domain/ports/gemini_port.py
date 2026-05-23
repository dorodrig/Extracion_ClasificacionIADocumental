import abc
from typing import Dict, Any

class GeminiPort(abc.ABC):
    @abc.abstractmethod
    async def resolve_ambiguities(self, data_package: Dict[str, Any], rule_pattern: str) -> Dict[str, Any]:
        """
        Analiza los datos extraídos y el patrón de la regla, devolviendo 
        los valores normalizados necesarios para construir la ruta, además
        del razonamiento seguido.
        """
        pass
