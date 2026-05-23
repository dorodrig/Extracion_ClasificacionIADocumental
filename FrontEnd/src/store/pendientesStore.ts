import { create } from 'zustand';
import { PendingDocument, DocumentViewerData, pendientesService } from '../services/pendientesService';

interface PendientesState {
  documentos: PendingDocument[];
  documentoSeleccionado: DocumentViewerData | null;
  isLoadingLista: boolean;
  isLoadingVisor: boolean;
  error: string | null;
  
  // Acciones
  fetchPendientes: () => Promise<void>;
  abrirVisor: (id: string) => Promise<void>;
  cerrarVisor: () => void;
  navegarVisor: (direccion: 'anterior' | 'siguiente') => Promise<void>;
  actualizarDocumentoWS: (doc: any) => void;
  nuevoDocumentoWS: (doc: PendingDocument) => void;
  setDocumentoEnReprocesamiento: (id: string) => void;
  eliminarDeCola: (id: string) => void;
}

export const usePendientesStore = create<PendientesState>((set, get) => ({
  documentos: [],
  documentoSeleccionado: null,
  isLoadingLista: false,
  isLoadingVisor: false,
  error: null,

  fetchPendientes: async () => {
    set({ isLoadingLista: true, error: null });
    try {
      const data = await pendientesService.getListaPendientes();
      set({ documentos: data, isLoadingLista: false });
    } catch (err: any) {
      set({ error: err.message, isLoadingLista: false });
    }
  },

  abrirVisor: async (id: string) => {
    set({ isLoadingVisor: true, error: null });
    try {
      const data = await pendientesService.getVisorDatos(id);
      set({ documentoSeleccionado: data, isLoadingVisor: false });
    } catch (err: any) {
      set({ error: err.message, isLoadingVisor: false });
    }
  },

  cerrarVisor: () => {
    set({ documentoSeleccionado: null });
  },

  navegarVisor: async (direccion: 'anterior' | 'siguiente') => {
    const { documentos, documentoSeleccionado, abrirVisor } = get();
    if (!documentoSeleccionado) return;

    const currentIndex = documentos.findIndex(d => d.id === documentoSeleccionado.id);
    if (currentIndex === -1) return;

    let nextIndex = direccion === 'anterior' ? currentIndex - 1 : currentIndex + 1;
    
    // Bounds check
    if (nextIndex >= 0 && nextIndex < documentos.length) {
      await abrirVisor(documentos[nextIndex].id);
    }
  },

  actualizarDocumentoWS: (docActualizado: any) => {
    // Si viene la actualizacion del agente y falló o se arregló
    set((state) => ({
      documentos: state.documentos.map(d => d.id === docActualizado.id ? { ...d, ...docActualizado } : d)
    }));
  },

  nuevoDocumentoWS: (nuevoDoc: PendingDocument) => {
    set((state) => ({
      documentos: [...state.documentos, nuevoDoc]
    }));
  },

  setDocumentoEnReprocesamiento: (id: string) => {
    set((state) => ({
      documentos: state.documentos.map(d => 
        d.id === id ? { ...d, motivoRechazo: '⟳ En reprocesamiento...' } : d
      )
    }));
  },

  eliminarDeCola: (id: string) => {
    set((state) => ({
      documentos: state.documentos.filter(d => d.id !== id),
      documentoSeleccionado: state.documentoSeleccionado?.id === id ? null : state.documentoSeleccionado
    }));
  }
}));
