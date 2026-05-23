/**
 * FolderTree — Recursive tree component for folder navigation
 * HU-07 — Portal de Consulta para Clientes
 */
import React, { useState } from 'react';
import { ChevronDown, ChevronRight, FolderOpen, FileText } from 'lucide-react';
import type { FolderNode } from '@/types/cliente';

export interface FolderTreeProps {
  node: FolderNode;
  selectedId: string | null;
  onSelect: (node: FolderNode) => void;
  depth?: number;
}

export const FolderTree: React.FC<FolderTreeProps> = ({
  node,
  selectedId,
  onSelect,
  depth = 0,
}) => {
  const [expanded, setExpanded] = useState(depth === 0);
  const isLeaf = !node.hijos || node.hijos.length === 0;
  const isSelected = node.id === selectedId;

  const handleClick = () => {
    onSelect(node);
    if (!isLeaf) {
      setExpanded((prev) => !prev);
    }
  };

  const depthClass =
    depth <= 5
      ? `grm-folder-tree__node--depth-${depth}`
      : 'grm-folder-tree__node--depth-deep';

  return (
    <div className="grm-folder-tree">
      <button
        className={`grm-folder-tree__node ${depthClass}${isSelected ? ' grm-folder-tree__node--selected' : ''}`}
        onClick={handleClick}
        type="button"
      >
        {!isLeaf ? (
          <span className="grm-folder-tree__toggle">
            {expanded ? (
              <ChevronDown size={14} />
            ) : (
              <ChevronRight size={14} />
            )}
          </span>
        ) : (
          <span className="grm-folder-tree__toggle grm-folder-tree__toggle--spacer" />
        )}

        {isLeaf ? (
          <FileText size={16} className="grm-folder-tree__icon grm-folder-tree__icon--file" />
        ) : (
          <FolderOpen size={16} className="grm-folder-tree__icon grm-folder-tree__icon--folder" />
        )}

        <span className="grm-folder-tree__label">{node.nombre}</span>
      </button>

      {!isLeaf && (
        <div
          className={`grm-folder-tree__children${expanded ? ' grm-folder-tree__children--expanded' : ''}`}
        >
          {node.hijos.map((child) => (
            <FolderTree
              key={child.id}
              node={child}
              selectedId={selectedId}
              onSelect={onSelect}
              depth={depth + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
};
