/**
 * RuleDynamicFields — Componente de campos dinámicos a extraer (CA-06)
 * Gobernanza §4.2 — Componente funcional + TypeScript estricto
 *
 * Permite agregar N campos con nombre, tipo de dato y obligatoriedad.
 * Valida nombres duplicados en tiempo real.
 */
import React, { useCallback } from 'react';
import {
  useFieldArray,
  useFormContext,
} from 'react-hook-form';
import { TIPOS_DATO_CAMPO, type RuleFormData } from '../../types/rule.types';
import styles from './RuleDynamicFields.module.scss';

export const RuleDynamicFields: React.FC = () => {
  const {
    control,
    register,
    watch,
    formState: { errors },
  } = useFormContext<RuleFormData>();

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'campos_extraer',
  });

  const watchFields = watch('campos_extraer');

  const handleAddField = useCallback(() => {
    append({ nombre: '', tipo: 'Texto', obligatorio: false });
  }, [append]);

  /**
   * Verifica si un nombre de campo está duplicado.
   * Comparación case-insensitive (alineado con validación backend).
   */
  const isDuplicate = (index: number): boolean => {
    if (!watchFields) return false;
    const currentName = watchFields[index]?.nombre?.trim().toLowerCase();
    if (!currentName) return false;
    return watchFields.some(
      (field, i) =>
        i !== index && field.nombre.trim().toLowerCase() === currentName
    );
  };

  return (
    <div className={styles['grm-dynamic-fields']}>
      <div className={styles['grm-dynamic-fields__header']}>
        <div className={styles['grm-dynamic-fields__title']}>
          <h4>Campos a Extraer</h4>
          <span className={styles['grm-dynamic-fields__required']}>*</span>
        </div>
        <button
          type="button"
          className={styles['grm-dynamic-fields__add-btn']}
          onClick={handleAddField}
        >
          + Agregar Campo
        </button>
      </div>

      {errors.campos_extraer && !Array.isArray(errors.campos_extraer) && (
        <p className={styles['grm-dynamic-fields__error']}>
          ⚠ {(errors.campos_extraer as { message?: string }).message}
        </p>
      )}

      {fields.length > 0 && (
        <div className={styles['grm-dynamic-fields__table']}>
          <div className={styles['grm-dynamic-fields__table-header']}>
            <span>Nombre del campo</span>
            <span>Tipo de dato</span>
            <span>Obligatorio</span>
            <span>Eliminar</span>
          </div>

          {fields.map((field, index) => {
            const duplicate = isDuplicate(index);
            const fieldErrors = errors.campos_extraer?.[index];

            return (
              <div
                key={field.id}
                className={`${styles['grm-dynamic-fields__row']} ${
                  duplicate ? styles['grm-dynamic-fields__row--duplicate'] : ''
                }`}
              >
                <div className={styles['grm-dynamic-fields__cell']}>
                  <input
                    {...register(`campos_extraer.${index}.nombre` as const, {
                      required: 'Nombre requerido',
                    })}
                    className={`${styles['grm-dynamic-fields__input']} ${
                      fieldErrors?.nombre || duplicate
                        ? styles['grm-dynamic-fields__input--error']
                        : ''
                    }`}
                    placeholder="Ej: Número de Cédula"
                  />
                  {fieldErrors?.nombre && (
                    <span className={styles['grm-dynamic-fields__field-error']}>
                      ⚠ {fieldErrors.nombre.message}
                    </span>
                  )}
                  {duplicate && (
                    <span className={styles['grm-dynamic-fields__field-warning']}>
                      ⚠ Nombre de campo duplicado
                    </span>
                  )}
                </div>

                <div className={styles['grm-dynamic-fields__cell']}>
                  <select
                    {...register(`campos_extraer.${index}.tipo` as const)}
                    className={styles['grm-dynamic-fields__select']}
                  >
                    {TIPOS_DATO_CAMPO.map((tipo) => (
                      <option key={tipo} value={tipo}>
                        {tipo}
                      </option>
                    ))}
                  </select>
                </div>

                <div
                  className={`${styles['grm-dynamic-fields__cell']} ${styles['grm-dynamic-fields__cell--center']}`}
                >
                  <label className={styles['grm-dynamic-fields__toggle']}>
                    <input
                      type="checkbox"
                      {...register(
                        `campos_extraer.${index}.obligatorio` as const
                      )}
                      className={styles['grm-dynamic-fields__toggle-input']}
                    />
                    <span className={styles['grm-dynamic-fields__toggle-slider']}></span>
                  </label>
                </div>

                <div
                  className={`${styles['grm-dynamic-fields__cell']} ${styles['grm-dynamic-fields__cell--center']}`}
                >
                  <button
                    type="button"
                    className={styles['grm-dynamic-fields__delete-btn']}
                    onClick={() => remove(index)}
                    title="Eliminar campo"
                    disabled={fields.length <= 1}
                  >
                    🗑
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {fields.length === 0 && (
        <div className={styles['grm-dynamic-fields__empty']}>
          <p>No hay campos definidos. Agrega al menos 1 campo a extraer.</p>
          <button
            type="button"
            className={styles['grm-dynamic-fields__add-btn']}
            onClick={handleAddField}
          >
            + Agregar Primer Campo
          </button>
        </div>
      )}

      <p className={styles['grm-dynamic-fields__note']}>
        Mínimo 1 campo requerido
      </p>
    </div>
  );
};
