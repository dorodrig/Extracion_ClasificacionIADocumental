import json
import logging
import google.generativeai as genai
from typing import Dict, Any

from app.domain.ports.gemini_port import GeminiPort
from app.core.config import settings
from app.core.exceptions import GeminiAPIException

logger = logging.getLogger("grm.ai_agents.gemini_adapter")

class GeminiAdapter(GeminiPort):
    def __init__(self):
        try:
            genai.configure(api_key=settings.gemini_api_key)
            # Utilizamos gemini-1.5-pro por defecto según lineamientos
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        except Exception as e:
            logger.critical(f"Error al configurar Gemini SDK: {str(e)}")
            raise GeminiAPIException(f"Error de configuración Gemini: {str(e)}")

    async def resolve_ambiguities(self, data_package: Dict[str, Any], rule_pattern: str) -> Dict[str, Any]:
        prompt = (
            "Eres un experto en clasificación y organización documental. "
            "Se te proporciona un conjunto de campos extraídos de un documento y un patrón de nombres de carpetas.\n"
            "Tu tarea es asignar el valor adecuado a cada variable en el patrón, resolviendo ambigüedades como "
            "abreviaciones en los nombres, formatos de número de identificación y tipo de documento.\n\n"
            f"Patrón de carpeta: {rule_pattern}\n"
            f"Datos extraídos (JSON):\n{json.dumps(data_package, ensure_ascii=False, indent=2)}\n\n"
            "Devuelve tu respuesta ÚNICAMENTE en formato JSON válido, sin delimitadores de código markdown (como ```json), "
            "que contenga exactamente las siguientes dos claves principales:\n"
            "1. 'variables_resueltas': un diccionario donde las claves son las variables del patrón (sin las llaves) "
            "y los valores son el resultado normalizado y en mayúsculas, usando 'SIN_DATO' si no es posible deducirlo.\n"
            "2. 'razonamiento': una breve cadena de texto explicando las decisiones tomadas para las variables ambiguas.\n"
        )

        try:
            # En la vida real, se usa `async` para Gemini pero python-generativeai soporta async via generate_content_async
            response = await self.model.generate_content_async(prompt)
            
            # Limpiar posible markdown o bloques ```json
            texto_respuesta = response.text.strip()
            if texto_respuesta.startswith("```json"):
                texto_respuesta = texto_respuesta[7:]
            if texto_respuesta.startswith("```"):
                texto_respuesta = texto_respuesta[3:]
            if texto_respuesta.endswith("```"):
                texto_respuesta = texto_respuesta[:-3]
            texto_respuesta = texto_respuesta.strip()
            
            resultado = json.loads(texto_respuesta)
            logger.info("Resolución de ambigüedades completada vía Gemini.")
            return resultado

        except json.JSONDecodeError as e:
            logger.error(f"Error parseando respuesta JSON de Gemini: {str(e)}. Respuesta original: {response.text}")
            raise GeminiAPIException("Gemini no devolvió un JSON válido.")
        except Exception as e:
            logger.error(f"Error al llamar a Gemini: {str(e)}")
            raise GeminiAPIException(f"Fallo en comunicación con Gemini: {str(e)}")
