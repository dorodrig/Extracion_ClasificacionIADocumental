import os
import shutil
import json
from pathlib import Path
from sqlalchemy.orm import Session
from app.db.repositories.clasificacion_repo import ClasificacionRepo
from app.db.models.documentos_pendientes import DocumentoPendiente
from app.services.gemini_adapter import GeminiAdapter
from app.core.config import settings

class ClasificacionIAService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ClasificacionRepo(db)
        self.gemini = GeminiAdapter()
        self.base_dir = settings.temp_dir

    def clasificar_documento(self, payload: dict) -> dict:
        try:
            documento_id = payload.get("documento_id")
            cliente_id = payload.get("cliente_id")
            batch_id = payload.get("batch_id")
            regla_id = payload.get("regla_id")
            datos_extraidos = payload.get("datos_extraidos", {})
            texto_ocr = payload.get("texto_ocr", "")
            archivo_origen = payload.get("archivo_origen")

            # Validate missing data
            cc = datos_extraidos.get("CC")
            nombre = datos_extraidos.get("NOMBRE_COMPLETO")
            tipo = datos_extraidos.get("TIPO_DOCUMENTO")
            instruccion = payload.get("instruccion_correctiva")

            if not cc or not nombre or not tipo or instruccion:
                # Use Gemini to disambiguate or correct
                prompt = f"""
                Analiza el siguiente texto de OCR y extrae la información faltante o corrige según la instrucción.
                Datos actuales: CC={cc}, NOMBRE={nombre}, TIPO={tipo}
                Texto OCR: {texto_ocr}
                Instrucción correctiva del operario: {instruccion if instruccion else 'Ninguna'}
                
                Devuelve SOLO un JSON con las claves CC, NOMBRE_COMPLETO, y TIPO_DOCUMENTO.
                """
                resp = self.gemini.invoke(prompt)
                
                try:
                    # Parse json
                    extracted = json.loads(resp.texto.replace("```json", "").replace("```", "").strip())
                    cc = extracted.get("CC", cc)
                    nombre = extracted.get("NOMBRE_COMPLETO", nombre)
                    tipo = extracted.get("TIPO_DOCUMENTO", tipo)
                    
                    datos_extraidos["CC"] = cc
                    datos_extraidos["NOMBRE_COMPLETO"] = nombre
                    datos_extraidos["TIPO_DOCUMENTO"] = tipo
                except Exception as e:
                    pass

            if not cc: cc = "DESCONOCIDO"
            if not nombre: nombre = "DESCONOCIDO"
            if not tipo: tipo = "DESCONOCIDO"

            nombre_archivo = os.path.basename(archivo_origen)
            ruta_destino_relativa = f"{cc}/{nombre}/{tipo}/{nombre_archivo}"
            ruta_destino_absoluta = os.path.join(self.base_dir, "clasificados", cc, nombre, tipo, nombre_archivo)
            
            # File system operations
            Path(os.path.dirname(ruta_destino_absoluta)).mkdir(parents=True, exist_ok=True)
            
            # Duplicate handling
            base, ext = os.path.splitext(ruta_destino_absoluta)
            contador = 1
            while os.path.exists(ruta_destino_absoluta):
                ruta_destino_absoluta = f"{base}_{contador}{ext}"
                ruta_destino_relativa = f"{cc}/{nombre}/{tipo}/{os.path.basename(ruta_destino_absoluta)}"
                contador += 1
            
            # Copy file
            if os.path.exists(archivo_origen):
                shutil.copy2(archivo_origen, ruta_destino_absoluta)
            else:
                raise FileNotFoundError(f"Archivo origen no encontrado: {archivo_origen}")

            # Upsert DB
            doc_clasificado = self.repo.upsert_clasificacion(
                documento_id=documento_id,
                cliente_id=cliente_id,
                batch_id=batch_id,
                regla_id=regla_id,
                campos_extraidos=datos_extraidos,
                ruta_destino=ruta_destino_relativa,
                tipo_documento=tipo
            )

            return {"success": True, "documento_clasificado_id": doc_clasificado.id, "ruta": ruta_destino_relativa}

        except Exception as e:
            # Enviar a pendientes por error de disco u otro
            self.db.rollback()
            pen = DocumentoPendiente(
                cliente_id=payload.get("cliente_id"),
                batch_id=payload.get("batch_id"),
                documento_id=payload.get("documento_id"),
                motivo_rechazo=str(e),
                campos_extraidos_json=payload.get("datos_extraidos", {}),
                estado="pendiente"
            )
            self.db.add(pen)
            self.db.commit()
            return {"success": False, "error": str(e)}
