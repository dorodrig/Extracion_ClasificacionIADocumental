/**
 * RulesPage — Página principal de gestión de reglas (CA-01 a CA-06)
 * Gobernanza §4.2 — Componente funcional con React Query
 *
 * Orquesta:
 * - Estado A: Cliente sin reglas → Empty state + formulario vacío (CA-01)
 * - Estado B: Cliente con reglas → Tabla de reglas (CA-02)
 * - Flujo de creación/edición (CA-03, CA-04, CA-05, CA-06)
 */
import React, { useState, useCallback, useRef } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getRulesByClient } from '../services/ruleService';
import { useClientStore } from '../store/clientStore';
import { RuleList } from '../components/Rules/RuleList';
import { RuleForm } from '../components/Rules/RuleForm';
import type { Rule } from '../types/rule.types';
import styles from './RulesPage.module.scss';

export const RulesPage: React.FC = () => {
  const clienteId = useClientStore((state) => state.clienteId);
  const clienteNombre = useClientStore((state) => state.clienteNombre);

  const [showForm, setShowForm] = useState(false);
  const [editingRule, setEditingRule] = useState<Rule | null>(null);
  const formRef = useRef<HTMLDivElement>(null);

  // Fetch rules via React Query (CA-02, mitiga R-04)
  const {
    data: rules = [],
    isLoading,
    error,
  } = useQuery({
    queryKey: ['rules', clienteId],
    queryFn: () => getRulesByClient(clienteId),
    staleTime: 30000,
  });

  const hasRules = rules.length > 0;

  // --- Handlers ---
  const handleNewRule = useCallback(() => {
    setEditingRule(null);
    setShowForm(true);
    setTimeout(() => {
      formRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  }, []);

  const handleEdit = useCallback((rule: Rule) => {
    setEditingRule(rule);
    setShowForm(true);
    setTimeout(() => {
      formRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  }, []);

  const handleCancel = useCallback(() => {
    setShowForm(false);
    setEditingRule(null);
  }, []);

  const handleSaved = useCallback(() => {
    setShowForm(false);
    setEditingRule(null);
  }, []);

  // --- Loading State ---
  if (isLoading) {
    return (
      <div className={styles['grm-rules-page']}>
        <div className={styles['grm-rules-page__loading']}>
          <div className="grm-spinner"></div>
          <p>Cargando reglas de trabajo...</p>
        </div>
      </div>
    );
  }

  // --- Error State ---
  if (error) {
    return (
      <div className={styles['grm-rules-page']}>
        <div className={styles['grm-rules-page__error']}>
          <span className={styles['grm-rules-page__error-icon']}>⚠</span>
          <h3>Error al cargar las reglas</h3>
          <p>{(error as Error).message}</p>
          <p className={styles['grm-rules-page__error-hint']}>
            Verifica que el servidor backend esté disponible en{' '}
            <code>{import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}</code>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles['grm-rules-page']}>
      {/* Page Header */}
      <div className={styles['grm-rules-page__header']}>
        <div>
          <h2 className={styles['grm-rules-page__title']}>
            Reglas de Trabajo — Cliente: {clienteNombre}
          </h2>
          <p className={styles['grm-rules-page__subtitle']}>
            Administra las políticas de procesamiento de documentos y validaciones
            automáticas.
          </p>
        </div>
        {hasRules && (
          <button
            className={styles['grm-rules-page__new-btn']}
            onClick={handleNewRule}
            type="button"
          >
            + Nueva Regla
          </button>
        )}
      </div>

      {/* Estado A: Sin reglas (CA-01) */}
      {!hasRules && !showForm && (
        <div className={styles['grm-rules-page__empty-state']}>
          <div className={styles['grm-rules-page__empty-icon']}>
            <svg width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="16" y="8" width="48" height="64" rx="4" stroke="#8b949e" strokeWidth="2" fill="none"/>
              <line x1="26" y1="24" x2="54" y2="24" stroke="#8b949e" strokeWidth="2"/>
              <line x1="26" y1="34" x2="54" y2="34" stroke="#8b949e" strokeWidth="2"/>
              <line x1="26" y1="44" x2="42" y2="44" stroke="#8b949e" strokeWidth="2"/>
              <circle cx="56" cy="56" r="16" fill="#161b22" stroke="#2f81f7" strokeWidth="2"/>
              <path d="M50 56H62M56 50V62" stroke="#2f81f7" strokeWidth="2" strokeLinecap="round"/>
            </svg>
          </div>
          <h3 className={styles['grm-rules-page__empty-title']}>
            Sin reglas configuradas
          </h3>
          <p className={styles['grm-rules-page__empty-description']}>
            Este cliente no tiene reglas de trabajo. Crea la primera para comenzar
            el proceso.
          </p>
          <button
            className={styles['grm-rules-page__empty-btn']}
            onClick={handleNewRule}
            type="button"
          >
            + Crear Primera Regla
          </button>
        </div>
      )}

      {/* Estado B: Con reglas (CA-02) */}
      {hasRules && !showForm && (
        <RuleList rules={rules} onEdit={handleEdit} onNewRule={handleNewRule} />
      )}

      {/* Formulario de Creación/Edición (CA-03, CA-04, CA-05, CA-06) */}
      {(showForm || (!hasRules && !showForm)) && (
        <div ref={formRef}>
          {/* Show form automatically for empty state (CA-01) */}
          {(!hasRules || showForm) && (
            <>
              {!hasRules && (
                <div className={styles['grm-rules-page__info-banner']}>
                  <span className={styles['grm-rules-page__info-icon']}>ℹ</span>
                  Este cliente no tiene reglas configuradas. Crea la primera regla.
                </div>
              )}
              <RuleForm
                editingRule={editingRule}
                onCancel={hasRules ? handleCancel : () => {}}
                onSaved={handleSaved}
              />
            </>
          )}
        </div>
      )}

      {/* Bottom section: Intelligence + Import */}
      {hasRules && !showForm && (
        <div className={styles['grm-rules-page__bottom-cards']}>
          <div className={styles['grm-rules-page__info-card']}>
            <div className={styles['grm-rules-page__info-card-header']}>
              <span className={styles['grm-rules-page__info-card-icon']}>🤖</span>
              <h4>Inteligencia Documental</h4>
            </div>
            <p>
              Nuestras reglas ahora soportan <strong>reconocimiento de patrones
              mediante IA</strong>. Puede configurar validaciones lógicas complejas
              sin necesidad de código, simplemente arrastrando campos detectados.
            </p>
            <button className={styles['grm-rules-page__info-card-link']} type="button">
              Conocer más →
            </button>
          </div>

          <div className={styles['grm-rules-page__info-card']}>
            <div className={styles['grm-rules-page__info-card-header']}>
              <span className={styles['grm-rules-page__info-card-icon']}>📥</span>
              <h4>Importar Configuración</h4>
            </div>
            <p>
              ¿Tienes reglas en otro cliente? Importa el archivo JSON de
              configuración para clonar la estructura en segundos.
            </p>
            <button className={styles['grm-rules-page__info-card-link']} type="button">
              Importar →
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
