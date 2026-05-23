import { create } from 'zustand';

export type IngestMode = 'scanner' | 'carpeta' | null;

export interface DocumentItem {
  id: string;
  file: File | null; // null if simulated scan
  name: string;
  extension: string;
  pages: number;
  sizeMB: number;
  status: 'Listo' | 'Ilegible' | 'En cola' | 'Procesando' | 'Clasificado' | 'Pendiente revisión humana' | 'Error';
  selected: boolean;
}

interface BatchStore {
  activeBatchId: string | null;
  ingestMode: IngestMode;
  documentsList: DocumentItem[];
  batchStatus: 'idle' | 'processing' | 'completed' | 'error';
  batchProgress: { preparados: number; total: number } | null;
  omittedFilesBackend: string[];
  
  setIngestMode: (mode: IngestMode) => void;
  setActiveBatch: (batchId: string) => void;
  setBatchStatus: (status: 'idle' | 'processing' | 'completed' | 'error') => void;
  setBatchProgress: (progress: { preparados: number; total: number } | null) => void;
  setOmittedFilesBackend: (files: string[]) => void;
  addDocuments: (docs: DocumentItem[]) => void;
  removeDocument: (id: string) => void;
  toggleDocumentSelection: (id: string) => void;
  toggleAllSelection: (selected: boolean) => void;
  updateDocumentStatus: (id: string, status: DocumentItem['status']) => void;
  resetBatch: () => void;
}

export const useBatchStore = create<BatchStore>((set) => ({
  activeBatchId: null,
  ingestMode: 'carpeta', // Preselected based on rule
  documentsList: [],
  batchStatus: 'idle',
  batchProgress: null,
  omittedFilesBackend: [],

  setIngestMode: (mode) => set({ ingestMode: mode }),
  setActiveBatch: (batchId) => set({ activeBatchId: batchId }),
  setBatchStatus: (status) => set({ batchStatus: status }),
  setBatchProgress: (progress) => set({ batchProgress: progress }),
  setOmittedFilesBackend: (files) => set({ omittedFilesBackend: files }),
  
  addDocuments: (docs) => set((state) => ({ 
    documentsList: [...state.documentsList, ...docs] 
  })),
  
  removeDocument: (id) => set((state) => ({
    documentsList: state.documentsList.filter(doc => doc.id !== id)
  })),
  
  toggleDocumentSelection: (id) => set((state) => ({
    documentsList: state.documentsList.map(doc => 
      doc.id === id ? { ...doc, selected: !doc.selected } : doc
    )
  })),
  
  toggleAllSelection: (selected) => set((state) => ({
    documentsList: state.documentsList.map(doc => ({ ...doc, selected }))
  })),

  updateDocumentStatus: (id, status) => set((state) => ({
    documentsList: state.documentsList.map(doc =>
      doc.id === id ? { ...doc, status } : doc
    )
  })),
  
  resetBatch: () => set({
    activeBatchId: null,
    documentsList: [],
    batchStatus: 'idle'
  })
}));
