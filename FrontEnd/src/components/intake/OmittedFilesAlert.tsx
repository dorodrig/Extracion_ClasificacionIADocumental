import React from 'react';
import styles from './OmittedFilesAlert.module.scss';
import { AlertTriangle } from 'lucide-react';

interface OmittedFilesAlertProps {
  omittedFiles: string[];
  count: number;
}

export const OmittedFilesAlert: React.FC<OmittedFilesAlertProps> = ({ omittedFiles, count }) => {
  if (count === 0 || omittedFiles.length === 0) return null;

  return (
    <div className={styles['grm-omitted-alert']}>
      <AlertTriangle size={16} className={styles['grm-omitted-alert__icon']} />
      <div className={styles['grm-omitted-alert__content']}>
        <span className={styles['grm-omitted-alert__title']}>
          Se omitieron {count} archivo(s) con formato no compatible:
        </span>
        <ul className={styles['grm-omitted-alert__list']}>
          {omittedFiles.slice(0, 5).map((file, i) => (
            <li key={i}>{file}</li>
          ))}
          {omittedFiles.length > 5 && (
            <li>... y {omittedFiles.length - 5} más</li>
          )}
        </ul>
      </div>
    </div>
  );
};
