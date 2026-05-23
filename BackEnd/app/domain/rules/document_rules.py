ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif'}

def validar_formato(extension: str) -> bool:
    """Verifica si la extensión del documento está permitida."""
    # Remover el punto inicial si existe y convertir a minúsculas
    ext = extension.lower().strip()
    if ext.startswith('.'):
        ext = ext[1:]
    return ext in ALLOWED_EXTENSIONS
