/**
 * Servicio de Reglas de Trabajo — HU-01
 * Gobernanza §4.3 — Consume endpoints reales del backend
 */
import api from './api';
import type {
  APIResponse,
  Rule,
  RuleCreatePayload,
  RuleUpdatePayload,
} from '../types/rule.types';

/**
 * Obtiene todas las reglas activas de un cliente.
 * Endpoint: GET /api/v1/rules?cliente_id={clienteId}
 */
export async function getRulesByClient(clienteId: number): Promise<Rule[]> {
  const response = await api.get<APIResponse<Rule[]>>('/api/v1/rules', {
    params: { cliente_id: clienteId },
  });
  return response.data.data ?? [];
}

/**
 * Obtiene el detalle de una regla por ID.
 * Endpoint: GET /api/v1/rules/{id}
 */
export async function getRuleById(ruleId: number): Promise<Rule> {
  const response = await api.get<APIResponse<Rule>>(`/api/v1/rules/${ruleId}`);
  if (!response.data.data) {
    throw new Error(response.data.error ?? 'Regla no encontrada');
  }
  return response.data.data;
}

/**
 * Crea una nueva regla de trabajo.
 * Endpoint: POST /api/v1/rules
 */
export async function createRule(data: RuleCreatePayload): Promise<Rule> {
  const response = await api.post<APIResponse<Rule>>('/api/v1/rules', data);
  if (!response.data.data) {
    throw new Error(response.data.error ?? 'Error al crear la regla');
  }
  return response.data.data;
}

/**
 * Actualiza una regla de trabajo existente.
 * Endpoint: PUT /api/v1/rules/{id}
 */
export async function updateRule(ruleId: number, data: RuleUpdatePayload): Promise<Rule> {
  const response = await api.put<APIResponse<Rule>>(`/api/v1/rules/${ruleId}`, data);
  if (!response.data.data) {
    throw new Error(response.data.error ?? 'Error al actualizar la regla');
  }
  return response.data.data;
}
