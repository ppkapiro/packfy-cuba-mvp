import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import Dashboard from '../pages/Dashboard';
import { enviosAPI } from '../services/api';

// Mock del API
vi.mock('../services/api', () => ({
  enviosAPI: {
    getAll: vi.fn(),
    getStats: vi.fn(),
  },
}));

// Mock del AuthContext
const mockAuthContext = {
  user: { id: 1, username: 'testuser', email: 'test@example.com' },
  isAuthenticated: true,
  login: vi.fn(),
  logout: vi.fn(),
  loading: false,
};

vi.mock('../contexts/AuthContext', () => ({
  useAuth: () => mockAuthContext,
}));

const renderDashboard = () => {
  return render(
    <BrowserRouter>
      <Dashboard />
    </BrowserRouter>
  );
};

describe('Dashboard Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();

    // Mock successful API responses
    (enviosAPI.getAll as any).mockResolvedValue({
      data: {
        results: [
          {
            id: 1,
            numero_guia: 'PK001',
            estado_actual: 'PENDIENTE',
            remitente_nombre: 'Juan Pérez',
            destinatario_nombre: 'María García',
            fecha_creacion: '2025-08-15T10:00:00Z',
            fecha_estimada_entrega: '2025-08-20',
            peso: 2.5,
            valor_declarado: 100.00
          }
        ],
        count: 1,
      }
    });

    (enviosAPI.getStats as any).mockResolvedValue({
      data: {
        total: 100,
        pendientes: 20,
        en_transito: 30,
        entregados: 45,
        cancelados: 5
      }
    });
  });

  it('debe renderizar el título principal del dashboard', async () => {
    renderDashboard();

    expect(screen.getByText('📊 Dashboard Principal')).toBeInTheDocument();
  });

  it('debe mostrar las estadísticas cuando se cargan los datos', async () => {
    renderDashboard();

    await waitFor(() => {
      expect(screen.getByText('Total de Envíos')).toBeInTheDocument();
    });

    // Verificar que se muestran las estadísticas
    expect(screen.getByText('100')).toBeInTheDocument(); // Total
    expect(screen.getByText('20')).toBeInTheDocument(); // Pendientes
  });

  it('debe cargar y mostrar la lista de envíos', async () => {
    renderDashboard();

    await waitFor(() => {
      expect(screen.getByText('PK001')).toBeInTheDocument();
    });

    expect(screen.getByText('Juan Pérez')).toBeInTheDocument();
    expect(screen.getByText('María García')).toBeInTheDocument();
  });

  it('debe manejar errores de carga graciosamente', async () => {
    // Mock error en API
    (enviosAPI.getAll as any).mockRejectedValue(new Error('Network error'));

    renderDashboard();

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });

  it('debe mostrar loading state inicialmente', () => {
    renderDashboard();

    // Debe mostrar algún indicador de carga
    expect(screen.getByTestId('loading-spinner') || screen.getByText(/cargando/i)).toBeInTheDocument();
  });

  it('debe llamar a las APIs correctamente al montar', async () => {
    renderDashboard();

    await waitFor(() => {
      expect(enviosAPI.getAll).toHaveBeenCalledWith(1, 10);
    });

    expect(enviosAPI.getStats).toHaveBeenCalled();
  });
});
