/**
 * Tipos TypeScript para Reglas de Trabajo — HU-01
 * Espejo de schemas Pydantic del backend (rule_schema.py)
 * Gobernanza §4.2 — Tipado estricto, sin `any`.
 */

// --- Campo a Extraer ---
export interface CampoExtraer {
  nombre: string;
  tipo: 'Texto' | 'Número' | 'Fecha' | 'Identificación';
  obligatorio: boolean;
}

// --- Respuesta de Regla (RuleResponse del backend) ---
export interface Rule {
  id: number;
  cliente_id: number;
  nombre: string;
  tipo_documento: string;
  campos_extraer: CampoExtraer[];
  patron_carpeta: string;
  modo_entrada: 'scanner' | 'carpeta';
  umbral_ocr: number;
  version: number;
  activa: boolean;
  created_by: number | null;
  created_at: string;
  updated_at: string | null;
}

// --- Creación de Regla (RuleCreate del backend) ---
export interface RuleCreatePayload {
  cliente_id: number;
  nombre: string;
  tipo_documento: string;
  campos_extraer: CampoExtraer[];
  patron_carpeta: string;
  modo_entrada: 'scanner' | 'carpeta';
}

// --- Actualización de Regla (RuleUpdate del backend — sin cliente_id) ---
export interface RuleUpdatePayload {
  nombre: string;
  tipo_documento: string;
  campos_extraer: CampoExtraer[];
  patron_carpeta: string;
  modo_entrada: 'scanner' | 'carpeta';
}

// --- Wrapper genérico de respuesta API (APIResponse del backend) ---
export interface APIResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

// --- Datos del formulario de regla (usado internamente por react-hook-form) ---
export interface RuleFormData {
  nombre: string;
  tipo_documento: string;
  modo_entrada: 'scanner' | 'carpeta';
  campos_extraer: CampoExtraer[];
  patron_carpeta: string;
}

// --- Tipos de documento disponibles ---
export const TIPOS_DOCUMENTO = [
  'Pagaré',
  'Endoso',
  'Cédula de Ciudadanía',
  'Carta Laboral',
] as const;

// --- Tipos de dato para campos a extraer ---
export const TIPOS_DATO_CAMPO: CampoExtraer['tipo'][] = [
  'Texto',
  'Número',
  'Fecha',
  'Identificación',
];

// --- Variables de patrón de carpeta disponibles ---
export const VARIABLES_PATRON = [
  'CC',
  'NOMBRE_COMPLETO',
  'TIPO_DOCUMENTO',
  'NOMBRE_ARCHIVO',
] as const;
