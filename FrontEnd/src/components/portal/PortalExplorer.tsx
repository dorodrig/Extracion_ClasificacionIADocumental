/**
 * PortalExplorer — Split-panel folder explorer
 * HU-07 — Portal de Consulta para Clientes
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FolderOpen, FileText, Eye } from 'lucide-react';
import { useClienteCarpetas } from '@/hooks/useClienteCarpetas';
import { FolderTree } from '@/components/portal/FolderTree';
import type { FolderNode } from '@/types/cliente';

export const PortalExplorer: React.FC = () => {
  const navigate = useNavigate();
  const { data, isLoading } = useClienteCarpetas();
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [selectedNode, setSelectedNode] = useState<FolderNode | null>(null);

  const handleSelect = (node: FolderNode) => {
    setSelectedId(node.id);
    setSelectedNode(node);
  };

  return (
    <div className="grm-portal-explorer">
      {/* Tree panel */}
      <div className="grm-portal-explorer__tree-panel">
        <h3 className="grm-portal-explorer__panel-title">
          Explorador de Carpetas
        </h3>
        {isLoading ? (
          <div className="grm-portal-explorer__skeleton">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="grm-portal-explorer__skeleton-row" />
            ))}
          </div>
        ) : data ? (
          <FolderTree
            node={data}
            selectedId={selectedId}
            onSelect={handleSelect}
          />
        ) : (
          <p className="grm-portal-explorer__no-data">
            No se encontraron carpetas.
          </p>
        )}
      </div>

      {/* Content panel */}
      <div className="grm-portal-explorer__content-panel">
        {selectedNode ? (
          <div className="grm-portal-explorer__content">
            <h3 className="grm-portal-explorer__content-title">
              <FolderOpen size={20} />
              {selectedNode.nombre}
            </h3>

            {selectedNode.hijos && selectedNode.hijos.length > 0 ? (
              <div className="grm-portal-explorer__file-grid">
                {selectedNode.hijos.map((child) => (
                  <div key={child.id} className="grm-portal-explorer__file-card">
                    <div className="grm-portal-explorer__file-card-icon">
                      {child.hijos && child.hijos.length > 0 ? (
                        <FolderOpen size={28} />
                      ) : (
                        <FileText size={28} />
                      )}
                    </div>
                    <span className="grm-portal-explorer__file-card-name">
                      {child.nombre}
                    </span>
                    {(!child.hijos || child.hijos.length === 0) && (
                      <button
                        className="grm-portal-explorer__file-card-btn"
                        onClick={() => navigate(`/cliente/visor/${child.id}`)}
                      >
                        <Eye size={14} /> Ver
                      </button>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="grm-portal-explorer__empty-folder">
                Esta carpeta está vacía
              </p>
            )}
          </div>
        ) : (
          <div className="grm-portal-explorer__empty">
            <FolderOpen size={48} className="grm-portal-explorer__empty-icon" />
            <p>Seleccione una carpeta para ver su contenido</p>
          </div>
        )}
      </div>
    </div>
  );
};
