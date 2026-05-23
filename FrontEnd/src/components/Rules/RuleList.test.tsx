/**
 * Tests unitarios — RuleList (CA-01, CA-02)
 * Valida: lista vacía, lista con datos, paginación, drawer de detalle.
 */
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { RuleList } from './RuleList';
import type { Rule } from '../../types/rule.types';

// --- Datos de prueba ---
const makeRule = (overrides: Partial<Rule> = {}): Rule => ({
  id: 1,
  cliente_id: 1,
  nombre: 'Regla de Prueba',
  tipo_documento: 'Pagaré',
  campos_extraer: [
    { nombre: 'Número', tipo: 'Identificación', obligatorio: true },
  ],
  patron_carpeta: '/{CC}/{TIPO_DOCUMENTO}',
  modo_entrada: 'scanner',
  umbral_ocr: 95,
  version: 1,
  activa: true,
  created_by: null,
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
  ...overrides,
});

const mockRulesMultiple: Rule[] = [
  makeRule({ id: 1, nombre: 'Regla Cédulas', tipo_documento: 'Cédula de Ciudadanía', version: 2 }),
  makeRule({ id: 2, nombre: 'Regla Pagarés', tipo_documento: 'Pagaré', modo_entrada: 'carpeta', version: 1 }),
  makeRule({ id: 3, nombre: 'Regla Endosos', tipo_documento: 'Endoso', version: 4 }),
];

let onEditMock: ReturnType<typeof vi.fn>;
let onNewRuleMock: ReturnType<typeof vi.fn>;

beforeEach(() => {
  onEditMock = vi.fn();
  onNewRuleMock = vi.fn();
});

// --- CA-01: Primer acceso sin reglas ---
describe('RuleList — CA-01: Lista vacía', () => {
  it('muestra "00" en el contador de reglas activas cuando no hay reglas', () => {
    render(<RuleList rules={[]} onEdit={onEditMock} onNewRule={onNewRuleMock} />);

    expect(screen.getByText('00')).toBeInTheDocument();
  });

  it('renderiza solo la fila de cabecera de la tabla (sin filas de datos)', () => {
    render(<RuleList rules={[]} onEdit={onEditMock} onNewRule={onNewRuleMock} />);

    // La tabla tiene un thead con una fila
    const rows = screen.getAllByRole('row');
    expect(rows).toHaveLength(1); // solo header
  });

  it('no renderiza controles de paginación con lista vacía', () => {
    render(<RuleList rules={[]} onEdit={onEditMock} onNewRule={onNewRuleMock} />);

    expect(screen.queryByText(/Anterior/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Siguiente/i)).not.toBeInTheDocument();
  });
});

// --- CA-02: Listado con reglas existentes ---
describe('RuleList — CA-02: Lista con datos', () => {
  it('muestra el conteo correcto de reglas en la stat card', () => {
    render(<RuleList rules={mockRulesMultiple} onEdit={onEditMock} onNewRule={onNewRuleMock} />);

    expect(screen.getByText('03')).toBeInTheDocument();
  });

  it('renderiza una fila por cada regla más la cabecera', () => {
    render(<RuleList rules={mockRulesMultiple} onEdit={onEditMock} onNewRule={onNewRuleMock} />);

    const rows = screen.getAllByRole('row');
    // 1 header + 3 data rows = 4
    expect(rows).toHaveLength(4);
  });

  it('muestra nombre, tipo de documento y badge de versión de cada regla', () => {
    render(<RuleList rules={mockRulesMultiple} onEdit={onEditMock} onNewRule={onNewRuleMock} />);

    expect(screen.getByText('Regla Cédulas')).toBeInTheDocument();
    expect(screen.getByText('Regla Pagarés')).toBeInTheDocument();
    expect(screen.getByText('Regla Endosos')).toBeInTheDocument();
    expect(screen.getByText('Cédula de Ciudadanía')).toBeInTheDocument();
    expect(screen.getByText('v2')).toBeInTheDocument();
    expect(screen.getByText('v4')).toBeInTheDocument();
  });

  it('muestra badges de modo de entrada correctamente (Escáner / Carpeta)', () => {
    render(<RuleList rules={mockRulesMultiple} onEdit={onEditMock} onNewRule={onNewRuleMock} />);

    // Dos reglas con scanner, una con carpeta
    const scannerBadges = screen.getAllByText(/Escáner/i);
    const carpetaBadges = screen.getAllByText(/Carpeta/i);

    expect(scannerBadges.length).toBe(2);
    expect(carpetaBadges.length).toBe(1);
  });

  it('llama a onEdit al hacer clic en el botón "Editar"', async () => {
    const user = userEvent.setup();
    render(<RuleList rules={mockRulesMultiple} onEdit={onEditMock} onNewRule={onNewRuleMock} />);

    const editButtons = screen.getAllByRole('button', { name: /Editar/i });
    await user.click(editButtons[0]);

    expect(onEditMock).toHaveBeenCalledTimes(1);
    expect(onEditMock).toHaveBeenCalledWith(mockRulesMultiple[0]);
  });

  it('abre el drawer de detalle al hacer clic en el botón "👁"', async () => {
    const user = userEvent.setup();
    render(<RuleList rules={mockRulesMultiple} onEdit={onEditMock} onNewRule={onNewRuleMock} />);

    const detailButtons = screen.getAllByRole('button', { name: '👁' });
    await user.click(detailButtons[0]);

    // El drawer debe mostrar los detalles de la regla (el nombre aparece en tabla + drawer)
    const ruleNameElements = screen.getAllByText('Regla Cédulas');
    expect(ruleNameElements.length).toBeGreaterThanOrEqual(2); // tabla + drawer

    // Verificar que el drawer muestra la etiqueta de Umbral OCR
    expect(screen.getByText('Umbral OCR')).toBeInTheDocument();
  });
});
