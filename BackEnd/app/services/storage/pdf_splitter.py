import os
from pypdf import PdfReader, PdfWriter
from app.domain.ports.pdf_splitter_port import PDFSplitterPort
from app.core.exceptions import PDFSplittingException

class PyPDFSplitterAdapter(PDFSplitterPort):
    def split_pdf(self, source_path: str, output_dir: str, batch_id: str, doc_id: int) -> list[str]:
        try:
            reader = PdfReader(source_path)
            total_pages = len(reader.pages)
            segmented_files = []
            
            for page_num in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[page_num])
                
                output_filename = f"{batch_id}_doc_{doc_id}_p{page_num + 1}.pdf"
                output_path = os.path.join(output_dir, output_filename)
                
                with open(output_path, "wb") as output_file:
                    writer.write(output_file)
                
                segmented_files.append(output_path)
                
            return segmented_files
        except Exception as e:
            raise PDFSplittingException(f"Error al segmentar el PDF {source_path}: {str(e)}")
