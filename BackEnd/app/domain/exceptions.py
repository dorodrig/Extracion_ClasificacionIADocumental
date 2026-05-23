"""
Excepciones de dominio del proyecto GRM.

Gobernanza §3.3 — Excepciones de dominio tipadas (GRMException).
Todas las excepciones de negocio heredan de GRMException para ser
capturadas por el exception handler global de FastAPI.
"""


class GRMException(Exception):
    """Excepción base del proyecto GRM."""
    pass


class RuleNotFoundException(GRMException):
    """La regla de trabajo solicitada no existe o no está activa."""

    def __init__(self, rule_id: int):
        self.rule_id = rule_id
        super().__init__(f"La regla de trabajo con id={rule_id} no fue encontrada.")


class DuplicateFieldNameException(GRMException):
    """
    Dos o más campos dentro de campos_extraer tienen el mismo nombre.

    CA-06: Validación case-insensitive de nombres duplicados.
    """

    def __init__(self, field_name: str):
        self.field_name = field_name
        super().__init__(
            f"El nombre de campo '{field_name}' está duplicado dentro de "
            f"campos_extraer. Los nombres deben ser únicos (case-insensitive)."
        )


class InvalidModoEntradaException(GRMException):
    """El modo de entrada proporcionado no es válido."""

    def __init__(self, modo: str):
        self.modo = modo
        super().__init__(
            f"El modo de entrada '{modo}' no es válido. "
            f"Valores permitidos: 'scanner', 'carpeta'."
        )


class RuleNameAlreadyExistsException(GRMException):
    """Ya existe una regla con el mismo nombre para este cliente."""

    def __init__(self, nombre: str, cliente_id: int):
        self.nombre = nombre
        self.cliente_id = cliente_id
        super().__init__(
            f"Ya existe una regla con el nombre '{nombre}' "
            f"para el cliente con id={cliente_id}."
        )


class InvalidPatronCarpetaException(GRMException):
    """El patrón de carpeta no contiene variables válidas de los campos a extraer."""

    def __init__(self, patron: str):
        self.patron = patron
        super().__init__(
            f"El patrón de carpeta '{patron}' es inválido. "
            f"Debe contener al menos una variable {{campo}} que corresponda a "
            f"un campo definido en campos_extraer."
        )
