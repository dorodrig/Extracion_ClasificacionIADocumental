/**
 * RuleList — Listado de reglas de trabajo en tabla (CA-02)
 * Gobernanza §4.2 — Componente funcional, tipado estricto
 *
 * Muestra la tabla de reglas existentes con acciones (Editar, Iniciar Proceso, Ver Detalle).
 * Incluye panel lateral (drawer) de solo lectura para detalle.
 */
import React, { useState, useMemo } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import { duplicateRule } from '../../services/ruleService';
import type { Rule } from '../../types/rule.types';
import styles from './RuleList.module.scss';

interface RuleListProps {
  rules: Rule[];
  onEdit: (rule: Rule) => void;
  onNewRule: () => void;
}

/**
 * Formatea una fecha ISO a "Hace X días/horas" con fecha exacta en hover.
 */
function formatRelativeDate(dateStr: string | null): { relative: string; exact: string } {
  if (!dateStr) return { relative: '—', exact: '—' };
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);
  const diffWeeks = Math.floor(diffDays / 7);

  let relative: string;
  if (diffMins < 1) relative = 'Ahora mismo';
  else if (diffMins < 60) relative = `Hace ${diffMins} min`;
  else if (diffHours < 24) relative = `Hace ${diffHours} hora${diffHours > 1 ? 's' : ''}`;
  else if (diffDays < 7) relative = `Hace ${diffDays} día${diffDays > 1 ? 's' : ''}`;
  else relative = `Hace ${diffWeeks} semana${diffWeeks > 1 ? 's' : ''}`;

  const exact = date.toLocaleDateString('es-CO', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  return { relative, exact };
}

const ITEMS_PER_PAGE = 10;

export const RuleList: React.FC<RuleListProps> = ({ rules, onEdit, onNewRule: _onNewRule }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [detailRule, setDetailRule] = useState<Rule | null>(null);
  
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const duplicateMutation = useMutation({
    mutationFn: (ruleId: number) => duplicateRule(ruleId),
    onSuccess: () => {
      toast.success('✓ Regla duplicada exitosamente');
      queryClient.invalidateQueries({ queryKey: ['rules'] });
    },
    onError: (error: Error) => {
      toast.error(`✗ ${error.message}`);
    },
  });

  const totalPages = Math.ceil(rules.length / ITEMS_PER_PAGE);
  const paginatedRules = useMemo(
    () =>
      rules.slice(
        (currentPage - 1) * ITEMS_PER_PAGE,
        currentPage * ITEMS_PER_PAGE
      ),
    [rules, currentPage]
  );

  const handleStartProcess = (rule: Rule) => {
    navigate(`/ingesta?rule_id=${rule.id}`);
  };

  return (
    <>
      <div className={styles['grm-rule-list']}>
        {/* Stats Cards */}
        <div className={styles['grm-rule-list__stats']}>
          <div className={styles['grm-rule-list__stat-card']}>
            <span className={styles['grm-rule-list__stat-icon']}>📊</span>
            <div className={styles['grm-rule-list__stat-content']}>
              <span className={styles['grm-rule-list__stat-label']}>Reglas Activas</span>
              <span className={styles['grm-rule-list__stat-value']}>{String(rules.length).padStart(2, '0')}</span>
            </div>
          </div>
          <div className={styles['grm-rule-list__stat-card']}>
            <span className={styles['grm-rule-list__stat-icon']}>✅</span>
            <div className={styles['grm-rule-list__stat-content']}>
              <span className={styles['grm-rule-list__stat-label']}>Validaciones Hoy</span>
              <span className={styles['grm-rule-list__stat-value']}>1,248</span>
            </div>
          </div>
          <div className={styles['grm-rule-list__stat-card']}>
            <span className={styles['grm-rule-list__stat-icon']}>⚡</span>
            <div className={styles['grm-rule-list__stat-content']}>
              <span className={styles['grm-rule-list__stat-label']}>Tiempo Promedio</span>
              <span className={styles['grm-rule-list__stat-value']}>0.4s</span>
            </div>
          </div>
        </div>

        {/* Table */}
        <div className={styles['grm-rule-list__table-container']}>
          <table className={styles['grm-rule-list__table']}>
            <thead>
              <tr>
                <th>Nombre de Regla</th>
                <th>Tipo de Documento</th>
                <th>Modo de Entrada</th>
                <th>Última Modificación</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {paginatedRules.map((rule) => {
                const dateInfo = formatRelativeDate(rule.updated_at ?? rule.created_at);
                return (
                  <tr key={rule.id}>
                    <td>
                      <div className={styles['grm-rule-list__name-cell']}>
                        <span className={styles['grm-rule-list__rule-name']}>
                          {rule.nombre}
                        </span>
                        <span className={styles['grm-rule-list__version-badge']}>
                          v{rule.version}
                        </span>
                      </div>
                    </td>
                    <td>{rule.tipo_documento}</td>
                    <td>
                      <span
                        className={`${styles['grm-rule-list__mode-badge']} ${
                          rule.modo_entrada === 'scanner'
                            ? styles['grm-rule-list__mode-badge--scanner']
                            : styles['grm-rule-list__mode-badge--carpeta']
                        }`}
                      >
                        {rule.modo_entrada === 'scanner' ? '🖨' : '📁'}{' '}
                        {rule.modo_entrada === 'scanner' ? 'Escáner' : 'Carpeta'}
                      </span>
                    </td>
                    <td title={dateInfo.exact}>
                      {dateInfo.relative}
                    </td>
                    <td>
                      <div className={styles['grm-rule-list__actions']}>
                        <button
                          className={styles['grm-rule-list__btn-process']}
                          onClick={() => handleStartProcess(rule)}
                          type="button"
                        >
                          ▶ Iniciar Proceso
                        </button>
                        <button
                          className={styles['grm-rule-list__btn-edit']}
                          onClick={() => onEdit(rule)}
                          type="button"
                        >
                          ✏ Editar
                        </button>
                        <button
                          className={styles['grm-rule-list__btn-duplicate']}
                          onClick={() => duplicateMutation.mutate(rule.id)}
                          disabled={duplicateMutation.isPending}
                          type="button"
                          style={{ margin: '0 4px' }}
                        >
                          📋 Duplicar
                        </button>
                        <button
                          className={styles['grm-rule-list__btn-detail']}
                          onClick={() => setDetailRule(rule)}
                          type="button"
                        >
                          👁
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className={styles['grm-rule-list__pagination']}>
            <span className={styles['grm-rule-list__pagination-info']}>
              Mostrando {(currentPage - 1) * ITEMS_PER_PAGE + 1} a{' '}
              {Math.min(currentPage * ITEMS_PER_PAGE, rules.length)} de{' '}
              {rules.length} reglas de trabajo activas
            </span>
            <div className={styles['grm-rule-list__pagination-controls']}>
              <button
                className={styles['grm-rule-list__pagination-btn']}
                onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                disabled={currentPage === 1}
                type="button"
              >
                ← Anterior
              </button>
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <button
                  key={page}
                  className={`${styles['grm-rule-list__pagination-btn']} ${
                    page === currentPage ? styles['grm-rule-list__pagination-btn--active'] : ''
                  }`}
                  onClick={() => setCurrentPage(page)}
                  type="button"
                >
                  {page}
                </button>
              ))}
              <button
                className={styles['grm-rule-list__pagination-btn']}
                onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                disabled={currentPage === totalPages}
                type="button"
              >
                Siguiente →
              </button>
            </div>
          </div>
        )}
      </div>

      {/* === Drawer de Detalle (Solo lectura) === */}
      {detailRule && (
        <>
          <div
            className={styles['grm-drawer-overlay']}
            onClick={() => setDetailRule(null)}
          ></div>
          <aside className={styles['grm-drawer']}>
            <div className={styles['grm-drawer__header']}>
              <div className={styles['grm-drawer__title']}>
                <h3>{detailRule.nombre}</h3>
                <span className={styles['grm-drawer__version']}>v{detailRule.version}</span>
              </div>
              <button
                className={styles['grm-drawer__close']}
                onClick={() => setDetailRule(null)}
                type="button"
              >
                ✕
              </button>
            </div>

            <div className={styles['grm-drawer__body']}>
              <div className={styles['grm-drawer__field']}>
                <span className={styles['grm-drawer__label']}>Tipo de Documento</span>
                <span className={styles['grm-drawer__value']}>{detailRule.tipo_documento}</span>
              </div>

              <div className={styles['grm-drawer__field']}>
                <span className={styles['grm-drawer__label']}>Modo de Entrada</span>
                <span className={styles['grm-drawer__value']}>
                  {detailRule.modo_entrada === 'scanner' ? '🖨 Escáner' : '📁 Carpeta'}
                </span>
              </div>

              <div className={styles['grm-drawer__field']}>
                <span className={styles['grm-drawer__label']}>Patrón de Carpeta</span>
                <code className={styles['grm-drawer__value-mono']}>
                  {detailRule.patron_carpeta}
                </code>
              </div>

              <div className={styles['grm-drawer__field']}>
                <span className={styles['grm-drawer__label']}>Umbral OCR</span>
                <span className={styles['grm-drawer__value']}>{detailRule.umbral_ocr}%</span>
              </div>

              <div className={styles['grm-drawer__field']}>
                <span className={styles['grm-drawer__label']}>Campos a Extraer ({detailRule.campos_extraer.length})</span>
                <div className={styles['grm-drawer__fields-list']}>
                  {detailRule.campos_extraer.map((campo, idx) => (
                    <div key={idx} className={styles['grm-drawer__field-item']}>
                      <span className={styles['grm-drawer__field-name']}>{campo.nombre}</span>
                      <span className={styles['grm-drawer__field-type']}>{campo.tipo}</span>
                      {campo.obligatorio && (
                        <span className={styles['grm-drawer__field-required']}>Obligatorio</span>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              <div className={styles['grm-drawer__field']}>
                <span className={styles['grm-drawer__label']}>Creada</span>
                <span className={styles['grm-drawer__value']}>
                  {new Date(detailRule.created_at).toLocaleDateString('es-CO', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </span>
              </div>

              {detailRule.updated_at && (
                <div className={styles['grm-drawer__field']}>
                  <span className={styles['grm-drawer__label']}>Última modificación</span>
                  <span className={styles['grm-drawer__value']}>
                    {new Date(detailRule.updated_at).toLocaleDateString('es-CO', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                    })}
                  </span>
                </div>
              )}
            </div>

            <div className={styles['grm-drawer__footer']}>
              <button
                className={styles['grm-drawer__edit-btn']}
                onClick={() => {
                  setDetailRule(null);
                  onEdit(detailRule);
                }}
                type="button"
              >
                ✏ Editar esta Regla
              </button>
            </div>
          </aside>
        </>
      )}
    </>
  );
};
