/**
 * RuleForm — Formulario de creación/edición de Reglas de Trabajo (CA-01, CA-03, CA-04, CA-05)
 * Gobernanza §4.2 — Componente funcional, tipado estricto, react-hook-form + Zod
 */
import React, { useMemo, useEffect } from 'react';
import { useForm, FormProvider } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { createRule, updateRule } from '../../services/ruleService';
import { useClientStore } from '../../store/clientStore';
import {
  TIPOS_DOCUMENTO,
  VARIABLES_PATRON,
  type Rule,
  type RuleFormData,
} from '../../types/rule.types';
import { RuleDynamicFields } from './RuleDynamicFields';
import styles from './RuleForm.module.scss';

// --- Zod Validation Schema (CA-05) ---
const ruleFormSchema = z.object({
  nombre: z
    .string()
    .min(1, 'El nombre de la regla es obligatorio')
    .max(255, 'Máximo 255 caracteres'),
  tipo_documento: z
    .string()
    .min(1, 'El tipo de documento es obligatorio')
    .max(255, 'Máximo 255 caracteres'),
  modo_entrada: z.enum(['scanner', 'carpeta'], {
    message: 'Selecciona un modo de entrada',
  }),
  campos_extraer: z
    .array(
      z.object({
        nombre: z.string().min(1, 'El nombre del campo es obligatorio'),
        tipo: z.enum(['Texto', 'Número', 'Fecha', 'Identificación']),
        obligatorio: z.boolean(),
      })
    )
    .min(1, 'Debes definir al menos 1 campo a extraer'),
  patron_carpeta: z
    .string()
    .min(1, 'El patrón de carpeta de salida es obligatorio')
    .max(500, 'Máximo 500 caracteres'),
});

interface RuleFormProps {
  editingRule: Rule | null;
  onCancel: () => void;
  onSaved: () => void;
}

export const RuleForm: React.FC<RuleFormProps> = ({
  editingRule,
  onCancel,
  onSaved,
}) => {
  const clienteId = useClientStore((state) => state.clienteId);
  const queryClient = useQueryClient();
  const isEditing = editingRule !== null;

  const defaultValues: RuleFormData = useMemo(
    () => ({
      nombre: editingRule?.nombre ?? '',
      tipo_documento: editingRule?.tipo_documento ?? '',
      modo_entrada: editingRule?.modo_entrada ?? 'scanner',
      campos_extraer: editingRule?.campos_extraer ?? [
        { nombre: '', tipo: 'Texto', obligatorio: false },
      ],
      patron_carpeta:
        editingRule?.patron_carpeta ?? '/{CC}/{NOMBRE_COMPLETO}/{TIPO_DOCUMENTO}/{NOMBRE_ARCHIVO}',
    }),
    [editingRule]
  );

  const methods = useForm<RuleFormData>({
    resolver: zodResolver(ruleFormSchema),
    defaultValues,
    mode: 'onChange',
  });

  const {
    register,
    handleSubmit,
    watch,
    reset,
    setValue,
    setError,
    formState: { errors, isValid },
  } = methods;

  // Reset form when switching between create/edit modes
  useEffect(() => {
    reset(defaultValues);
  }, [defaultValues, reset]);

  // Watch patron for live preview
  const patronValue = watch('patron_carpeta');
  const camposExtraer = watch('campos_extraer');

  // Validate variables in patron_carpeta (CA-07)
  const invalidVariables = useMemo(() => {
    if (!patronValue) return [];
    const matches = patronValue.match(/\{([^}]+)\}/g);
    if (!matches) return [];
    
    const extractedNames = camposExtraer.map((c: any) => c.nombre);
    const validVars = [...VARIABLES_PATRON, ...extractedNames];
    
    const invalid = matches
      .map(m => m.replace(/[{}]/g, ''))
      .filter(v => !validVars.includes(v));
      
    return Array.from(new Set(invalid));
  }, [patronValue, camposExtraer]);

  // --- Mutations ---
  const createMutation = useMutation({
    mutationFn: (data: RuleFormData) => {
      const cleanCampos = data.campos_extraer.map(c => ({
        nombre: c.nombre,
        tipo: c.tipo,
        obligatorio: Boolean(c.obligatorio)
      }));
      return createRule({ ...data, campos_extraer: cleanCampos, cliente_id: Number(clienteId) });
    },
    onSuccess: () => {
      toast.success('✓ Regla guardada exitosamente');
      queryClient.invalidateQueries({ queryKey: ['rules', clienteId] });
      onSaved();
    },
    onError: (error: any) => {
      console.error('API Error:', error.response?.data);
      if (error?.response?.status === 409 || error.message.toLowerCase().includes('ya existe')) {
        setError('nombre', { type: 'manual', message: 'El nombre de la regla ya existe para este cliente' });
      } else {
        toast.error(`✗ ${error.message}`);
      }
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: RuleFormData) => {
      const cleanCampos = data.campos_extraer.map(c => ({
        nombre: c.nombre,
        tipo: c.tipo,
        obligatorio: Boolean(c.obligatorio)
      }));
      return updateRule(editingRule!.id, { ...data, campos_extraer: cleanCampos });
    },
    onSuccess: () => {
      toast.success('✓ Regla actualizada exitosamente');
      queryClient.invalidateQueries({ queryKey: ['rules', clienteId] });
      onSaved();
    },
    onError: (error: any) => {
      if (error?.response?.status === 409 || error.message.toLowerCase().includes('ya existe')) {
        setError('nombre', { type: 'manual', message: 'El nombre de la regla ya existe para este cliente' });
      } else {
        toast.error(`✗ ${error.message}`);
      }
    },
  });

  const isSubmitting = createMutation.isPending || updateMutation.isPending;

  const onSubmit = (data: RuleFormData) => {
    // Validar nombres duplicados en campos_extraer (CA-06)
    const nombres = data.campos_extraer.map((c) => c.nombre.trim().toLowerCase());
    const hasDuplicates = nombres.some(
      (name, idx) => nombres.indexOf(name) !== idx
    );
    if (hasDuplicates) {
      toast.error('✗ Existen nombres de campos duplicados');
      return;
    }

    if (isEditing) {
      updateMutation.mutate(data);
    } else {
      createMutation.mutate(data);
    }
  };

  /**
   * Genera la vista previa en tiempo real del patrón de carpeta
   */
  const patronPreview = useMemo(() => {
    if (!patronValue) return '';
    return patronValue
      .replace('{CC}', 'CC123456789')
      .replace('{NOMBRE_COMPLETO}', 'DAVID_RODRIGUEZ')
      .replace('{TIPO_DOCUMENTO}', 'PAGARE')
      .replace('{NOMBRE_ARCHIVO}', 'pagare_001.pdf');
  }, [patronValue]);

  const handleInsertVariable = (variable: string) => {
    const currentValue = watch('patron_carpeta');
    setValue('patron_carpeta', `${currentValue}{${variable}}`, {
      shouldValidate: true,
      shouldDirty: true,
    });
  };

  // --- Tipo de documento con opción personalizada ---
  const tipoDocumento = watch('tipo_documento');
  const isCustomTipo = tipoDocumento !== '' && !TIPOS_DOCUMENTO.includes(tipoDocumento as typeof TIPOS_DOCUMENTO[number]);

  return (
    <FormProvider {...methods}>
      <form
        className={styles['grm-rule-form']}
        onSubmit={handleSubmit(onSubmit)}
        noValidate
      >
        <div className={styles['grm-rule-form__header']}>
          <h3>{isEditing ? '✏ Editar Regla' : '+ Crear Nueva Regla'}</h3>
          {isEditing && editingRule && (
            <span className={styles['grm-rule-form__version-badge']}>
              v{editingRule.version}
            </span>
          )}
        </div>

        {/* === Sección 1: Información General === */}
        <section className={styles['grm-rule-form__section']}>
          <h4 className={styles['grm-rule-form__section-title']}>
            Información General
          </h4>

          <div className={styles['grm-rule-form__field']}>
            <label className={styles['grm-rule-form__label']}>
              Nombre de la Regla <span className={styles['grm-rule-form__required']}>*</span>
            </label>
            <input
              {...register('nombre')}
              className={`${styles['grm-rule-form__input']} ${
                errors.nombre ? styles['grm-rule-form__input--error'] : ''
              }`}
              placeholder="Ej: Pagarés Q1 2025"
            />
            {errors.nombre && (
              <p className={styles['grm-rule-form__error']}>
                ⚠ {errors.nombre.message}
              </p>
            )}
          </div>

          <div className={styles['grm-rule-form__field']}>
            <label className={styles['grm-rule-form__label']}>
              Tipo de Documento <span className={styles['grm-rule-form__required']}>*</span>
            </label>
            <div className={styles['grm-rule-form__select-with-custom']}>
              <select
                className={`${styles['grm-rule-form__select']} ${
                  errors.tipo_documento ? styles['grm-rule-form__select--error'] : ''
                }`}
                value={
                  TIPOS_DOCUMENTO.includes(tipoDocumento as typeof TIPOS_DOCUMENTO[number])
                    ? tipoDocumento
                    : tipoDocumento
                      ? '__custom__'
                      : ''
                }
                onChange={(e) => {
                  if (e.target.value === '__custom__') {
                    setValue('tipo_documento', '', { shouldValidate: true, shouldDirty: true });
                  } else {
                    setValue('tipo_documento', e.target.value, { shouldValidate: true, shouldDirty: true });
                  }
                }}
              >
                <option value="" disabled>
                  Seleccionar tipo...
                </option>
                {TIPOS_DOCUMENTO.map((tipo) => (
                  <option key={tipo} value={tipo}>
                    {tipo}
                  </option>
                ))}
                <option value="__custom__">Otro (personalizado)</option>
              </select>
              {isCustomTipo && (
                <input
                  {...register('tipo_documento')}
                  className={styles['grm-rule-form__input']}
                  placeholder="Escribe el tipo de documento..."
                  autoFocus
                />
              )}
            </div>
            {errors.tipo_documento && (
              <p className={styles['grm-rule-form__error']}>
                ⚠ {errors.tipo_documento.message}
              </p>
            )}
          </div>

          <div className={styles['grm-rule-form__field']}>
            <label className={styles['grm-rule-form__label']}>
              Modo de Entrada <span className={styles['grm-rule-form__required']}>*</span>
            </label>
            <div className={styles['grm-rule-form__radio-group']}>
              <label className={styles['grm-rule-form__radio']}>
                <input
                  type="radio"
                  value="scanner"
                  {...register('modo_entrada')}
                />
                <span className={styles['grm-rule-form__radio-indicator']}></span>
                <span className={styles['grm-rule-form__radio-label']}>
                  🖨 Escáner (por lotes)
                </span>
              </label>
              <label className={styles['grm-rule-form__radio']}>
                <input
                  type="radio"
                  value="carpeta"
                  {...register('modo_entrada')}
                />
                <span className={styles['grm-rule-form__radio-indicator']}></span>
                <span className={styles['grm-rule-form__radio-label']}>
                  📁 Carpeta local (uno a uno)
                </span>
              </label>
            </div>
            {errors.modo_entrada && (
              <p className={styles['grm-rule-form__error']}>
                ⚠ {errors.modo_entrada.message}
              </p>
            )}
          </div>
        </section>

        {/* === Sección 2: Campos a Extraer (CA-06) === */}
        <RuleDynamicFields />

        {/* === Sección 3: Patrón de Carpeta === */}
        <section className={styles['grm-rule-form__section']}>
          <h4 className={styles['grm-rule-form__section-title']}>
            Patrón de Carpeta de Salida <span className={styles['grm-rule-form__required']}>*</span>
          </h4>

          <div className={styles['grm-rule-form__chips']}>
            <span className={styles['grm-rule-form__chips-label']}>
              Variables disponibles:
            </span>
            {VARIABLES_PATRON.map((variable) => (
              <button
                key={variable}
                type="button"
                className={styles['grm-rule-form__chip']}
                onClick={() => handleInsertVariable(variable)}
              >
                {`{${variable}}`}
              </button>
            ))}
          </div>

          <div className={styles['grm-rule-form__field']}>
            <label className={styles['grm-rule-form__label']}>Patrón:</label>
            <input
              {...register('patron_carpeta')}
              className={`${styles['grm-rule-form__input']} ${styles['grm-rule-form__input--mono']} ${
                errors.patron_carpeta ? styles['grm-rule-form__input--error'] : ''
              }`}
              placeholder="/{CC}/{NOMBRE_COMPLETO}/{TIPO_DOCUMENTO}/{NOMBRE_ARCHIVO}"
            />
            {errors.patron_carpeta && (
              <p className={styles['grm-rule-form__error']}>
                ⚠ {errors.patron_carpeta.message}
              </p>
            )}
          </div>

          {patronPreview && (
            <div className={styles['grm-rule-form__preview']}>
              <span className={styles['grm-rule-form__preview-label']}>
                Vista previa en tiempo real:
              </span>
              <code className={styles['grm-rule-form__preview-path']}>
                📁 {patronPreview}
              </code>
            </div>
          )}
          {invalidVariables.length > 0 && (
            <p className={styles['grm-rule-form__error']} style={{ marginTop: '8px' }}>
              ⚠ Advertencia: Las siguientes variables no existen: {invalidVariables.map(v => `{${v}}`).join(', ')}
            </p>
          )}
        </section>

        {/* === Sección 4: Configuración OCR (Solo lectura) === */}
        <section className={styles['grm-rule-form__section']}>
          <h4 className={styles['grm-rule-form__section-title']}>
            Configuración OCR
          </h4>

          <div className={styles['grm-rule-form__ocr-config']}>
            <span className={styles['grm-rule-form__ocr-label']}>
              Umbral de Confianza OCR:
            </span>
            <div className={styles['grm-rule-form__ocr-bar']}>
              <div
                className={styles['grm-rule-form__ocr-bar-fill']}
                style={{ width: '95%' }}
              ></div>
            </div>
            <span className={styles['grm-rule-form__ocr-value']}>
              95% <span title="El sistema descartará campos con confianza inferior al 95%. Este valor es fijo por estándar del proceso GRM." style={{ cursor: 'help', color: '#6b7280', marginLeft: '4px' }}>ℹ</span>
            </span>
          </div>
          <p className={styles['grm-rule-form__ocr-info']}>
            El umbral de confianza está fijado al 95% para garantizar la calidad de extracción.
          </p>
        </section>

        {/* === Pie del formulario === */}
        <div className={styles['grm-rule-form__actions']}>
          <button
            type="button"
            className={styles['grm-rule-form__btn-cancel']}
            onClick={onCancel}
            disabled={isSubmitting}
          >
            Cancelar
          </button>
          <button
            type="submit"
            className={styles['grm-rule-form__btn-submit']}
            disabled={!isValid || isSubmitting}
            title={
              !isValid
                ? 'Completa los campos obligatorios marcados con *'
                : undefined
            }
          >
            {isSubmitting && <span className="grm-spinner"></span>}
            {isEditing ? 'Actualizar Regla' : 'Guardar Regla ▶'}
          </button>
        </div>
      </form>
    </FormProvider>
  );
};
