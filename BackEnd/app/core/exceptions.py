class GRMException(Exception):
    """Excepción base del proyecto GRM"""
    pass

class BatchCreationException(GRMException):
    pass

class InvalidDocumentFormatException(GRMException):
    pass

class PDFSplittingException(GRMException):
    pass

class StorageException(GRMException):
    pass
