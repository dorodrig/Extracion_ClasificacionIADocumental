/**
 * Tests unitarios — RuleForm (CA-01, CA-03, CA-04, CA-05, CA-06)
 * Valida: botón deshabilitado, habilitación tras completar campos, renderizado en modo edición.
 */
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { RuleForm } from './RuleForm';
import type { Rule } from '../../types/rule.types';

// --- Mocks ---
vi.mock('../../store/clientStore', () => ({
  useClientStore: vi.fn((selector: (state: any) => any) =>
    selector({ clienteId: 1, clienteNombre: 'TEST', operarioNombre: 'Test', operarioRol: 'Admin' })
  ),
}));

vi.mock('../../services/ruleService', () => ({
  createRule: vi.fn().mockResolvedValue({ id: 1 }),
  updateRule: vi.fn().mockResolvedValue({ id: 1 }),
}));

vi.mock('react-hot-toast', () => ({
  default: { success: vi.fn(), error: vi.fn() },
}));

// --- Helpers ---
let queryClient: QueryClient;

beforeEach(() => {
  queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
});

const renderRuleForm = (props: Partial<React.ComponentProps<typeof RuleForm>> = {}) => {
  const defaultProps = {
    editingRule: null,
    onCancel: vi.fn(),
    onSaved: vi.fn(),
  };
  return render(
    <QueryClientProvider client={queryClient}>
      <RuleForm {...defaultProps} {...props} />
    </QueryClientProvider>
  );
};

// --- CA-05: Botón "Guardar Regla" deshabilitado hasta completar campos ---
describe('RuleForm — CA-05: Validación de campos obligatorios', () => {
  it('el botón "Guardar Regla" está deshabilitado al iniciar (campos vacíos)', () => {
    renderRuleForm();

    const submitBtn = screen.getByRole('button', { name: /Guardar Regla/i });
    expect(submitBtn).toBeDisabled();
  });

  it('el botón se habilita tras completar todos los campos obligatorios', async () => {
    const user = userEvent.setup();
    renderRuleForm();

    // 1. Nombre de la Regla
    const nombreInput = screen.getByPlaceholderText(/Ej: Pagarés Q1 2025/i);
    await user.clear(nombreInput);
    await user.type(nombreInput, 'Regla Test QA');

    // 2. Tipo de Documento — seleccionar del dropdown
    const selects = screen.getAllByRole('combobox');
    await user.selectOptions(selects[0], 'Pagaré');

    // 3. Campo a extraer — el formulario ya trae uno por defecto vacío
    const campoInput = screen.getByPlaceholderText(/Ej: Número de Cédula/i);
    await user.clear(campoInput);
    await user.type(campoInput, 'Número de Cédula');

    // 4. Patrón de carpeta — ya tiene valor por defecto, verificar
    //    El default es '/{CC}/{NOMBRE_COMPLETO}/{TIPO_DOCUMENTO}/{NOMBRE_ARCHIVO}'

    // Esperar a que react-hook-form revalide y habilite el botón
    await waitFor(
      () => {
        const submitBtn = screen.getByRole('button', { name: /Guardar Regla/i });
        expect(submitBtn).not.toBeDisabled();
      },
      { timeout: 3000 }
    );
  });
});

// --- CA-01 / CA-03: Renderizado en modo creación vs edición ---
describe('RuleForm — CA-01/CA-03: Modos creación y edición', () => {
  it('muestra título "+ Crear Nueva Regla" en modo creación (CA-01)', () => {
    renderRuleForm({ editingRule: null });
    expect(screen.getByText(/Crear Nueva Regla/i)).toBeInTheDocument();
  });

  it('muestra título "Editar Regla" y carga datos en modo edición (CA-03)', () => {
    const editingRule: Rule = {
      id: 42,
      cliente_id: 1,
      nombre: 'Regla Existente',
      tipo_documento: 'Pagaré',
      campos_extraer: [
        { nombre: 'Número', tipo: 'Identificación', obligatorio: true },
      ],
      patron_carpeta: '/{CC}/{TIPO_DOCUMENTO}',
      modo_entrada: 'scanner',
      umbral_ocr: 95,
      version: 3,
      activa: true,
      created_by: null,
      created_at: '2026-01-01T00:00:00Z',
      updated_at: '2026-05-20T10:00:00Z',
    };

    renderRuleForm({ editingRule });

    expect(screen.getByText(/Editar Regla/i)).toBeInTheDocument();
    expect(screen.getByText('v3')).toBeInTheDocument();

    // El nombre precargado
    const nombreInput = screen.getByPlaceholderText(/Ej: Pagarés Q1 2025/i) as HTMLInputElement;
    expect(nombreInput.value).toBe('Regla Existente');
  });
});

// --- CA-06: FieldArray dinámico — agregar campos ---
describe('RuleForm — CA-06: Campos dinámicos a extraer', () => {
  it('agrega un nuevo campo al hacer clic en "+ Agregar Campo"', async () => {
    const user = userEvent.setup();
    renderRuleForm();

    // Inicialmente hay 1 campo vacío por defecto
    const initialInputs = screen.getAllByPlaceholderText(/Ej: Número de Cédula/i);
    expect(initialInputs).toHaveLength(1);

    // Clic en "+ Agregar Campo"
    const addBtn = screen.getByRole('button', { name: /\+ Agregar Campo/i });
    await user.click(addBtn);

    // Ahora debe haber 2
    await waitFor(() => {
      const updatedInputs = screen.getAllByPlaceholderText(/Ej: Número de Cédula/i);
      expect(updatedInputs).toHaveLength(2);
    });
  });

  it('muestra advertencia de duplicados al escribir nombres iguales (CA-06)', async () => {
    const user = userEvent.setup();
    renderRuleForm();

    // Agregar un segundo campo
    const addBtn = screen.getByRole('button', { name: /\+ Agregar Campo/i });
    await user.click(addBtn);

    const campos = screen.getAllByPlaceholderText(/Ej: Número de Cédula/i);

    // Escribir el mismo nombre en ambos campos
    await user.type(campos[0], 'Cédula');
    await user.type(campos[1], 'Cédula');

    // Debe aparecer advertencia de duplicado
    await waitFor(() => {
      const warnings = screen.getAllByText(/Nombre de campo duplicado/i);
      expect(warnings.length).toBeGreaterThanOrEqual(1);
    });
  });
});
