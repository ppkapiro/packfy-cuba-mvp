import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import GestionUnificada from '../pages/GestionUnificada';
import { enviosAPI } from '../services/api';

// Mock del API
vi.mock('../services/api', () => ({
  enviosAPI: {
    getAll: vi.fn(),
    updateStatus: vi.fn(),
    delete: vi.fn(),
  },
}));

// Mock del AuthContext
vi.mock('../contexts/AuthContext', () => ({
  useAuth: () => ({
    user: { id: 1, username: 'admin', email: 'admin@test.com' },
    isAuthenticated: true,
  }),
}));

const mockEnvios = [
  {
    id: 1,
    numero_guia: 'PK001',
    estado_actual: 'PENDIENTE',
    remitente_nombre: 'Juan Pérez',
    remitente_telefono: '+53 5555-1234',
    destinatario_nombre: 'María García',
    destinatario_telefono: '+53 5555-5678',
    fecha_creacion: '2025-08-15T10:00:00Z',
    peso: 2.5,
    valor_declarado: 100.00,
    descripcion: 'Paquete de prueba'
  },
  {
    id: 2,
    numero_guia: 'PK002',
    estado_actual: 'EN_TRANSITO',
    remitente_nombre: 'Carlos López',
    remitente_telefono: '+53 5555-2468',
    destinatario_nombre: 'Ana Martínez',
    destinatario_telefono: '+53 5555-1357',
    fecha_creacion: '2025-08-14T15:30:00Z',
    peso: 1.2,
    valor_declarado: 50.00,
    descripcion: 'Documentos importantes'
  }
];

const renderGestionUnificada = () => {
  return render(
    <BrowserRouter>
      <GestionUnificada />
    </BrowserRouter>
  );
};

describe('GestionUnificada Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();

    (enviosAPI.getAll as any).mockResolvedValue({
      data: mockEnvios
    });
  });

  it('debe renderizar el título de gestión de envíos', async () => {
    renderGestionUnificada();

    expect(screen.getByText('📦 Gestión de Envíos')).toBeInTheDocument();
    expect(screen.getByText('Administra todos los envíos del sistema desde un solo lugar')).toBeInTheDocument();
  });

  it('debe cargar y mostrar la lista de envíos', async () => {
    renderGestionUnificada();

    await waitFor(() => {
      expect(screen.getByText('PK001')).toBeInTheDocument();
      expect(screen.getByText('PK002')).toBeInTheDocument();
    });

    expect(screen.getByText('Juan Pérez')).toBeInTheDocument();
    expect(screen.getByText('María García')).toBeInTheDocument();
    expect(screen.getByText('Carlos López')).toBeInTheDocument();
  });

  it('debe mostrar estadísticas correctas', async () => {
    renderGestionUnificada();

    await waitFor(() => {
      expect(screen.getByText('2')).toBeInTheDocument(); // Total
    });

    // Verificar estadísticas por estado
    expect(screen.getByText('Pendientes')).toBeInTheDocument();
    expect(screen.getByText('En Tránsito')).toBeInTheDocument();
  });

  it('debe permitir buscar envíos', async () => {
    renderGestionUnificada();

    await waitFor(() => {
      expect(screen.getByText('PK001')).toBeInTheDocument();
    });

    const searchInput = screen.getByPlaceholderText('Buscar...');
    fireEvent.change(searchInput, { target: { value: 'PK001' } });

    await waitFor(() => {
      expect(screen.getByText('PK001')).toBeInTheDocument();
      expect(screen.queryByText('PK002')).not.toBeInTheDocument();
    });
  });

  it('debe permitir filtrar por estado', async () => {
    renderGestionUnificada();

    await waitFor(() => {
      expect(screen.getByText('PK001')).toBeInTheDocument();
    });

    // Buscar el select de filtro por estado
    const estadoSelect = screen.getByLabelText(/estado/i);
    fireEvent.change(estadoSelect, { target: { value: 'PENDIENTE' } });

    await waitFor(() => {
      expect(screen.getByText('PK001')).toBeInTheDocument();
      expect(screen.queryByText('PK002')).not.toBeInTheDocument();
    });
  });

  it('debe mostrar botón de refrescar', async () => {
    renderGestionUnificada();

    const refreshButton = screen.getByText('🔄 Refrescar');
    expect(refreshButton).toBeInTheDocument();

    fireEvent.click(refreshButton);
    expect(enviosAPI.getAll).toHaveBeenCalledTimes(2); // Initial load + refresh
  });

  it('debe manejar errores de carga', async () => {
    (enviosAPI.getAll as any).mockRejectedValue(new Error('API Error'));

    renderGestionUnificada();

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });

  it('debe mostrar loading state', () => {
    renderGestionUnificada();

    // Verificar que se muestra algún indicador de carga
    expect(screen.getByText(/cargando/i) || screen.getByTestId('loading-skeleton')).toBeInTheDocument();
  });
});
