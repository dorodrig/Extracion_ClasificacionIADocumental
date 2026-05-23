import abc

class PDFSplitterPort(abc.ABC):
    @abc.abstractmethod
    def split_pdf(self, source_path: str, output_dir: str, batch_id: str, doc_id: int) -> list[str]:
        """
        Divide un PDF en páginas individuales y las guarda en el output_dir.
        Retorna la lista de rutas a las páginas segmentadas.
        """
        pass
