import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import ShipmentDetail from '../ShipmentDetail';
import { vi } from 'vitest';

// Mock del módulo de API utilizado por el componente
vi.mock('../../services/api', () => ({
  enviosAPI: {
    getById: vi.fn(),
    update: vi.fn(),
  },
}));

// Ayudante para promesa diferida
const deferred = <T,>() => {
  let resolve!: (v: T) => void;
  let reject!: (e: any) => void;
  const promise = new Promise<T>((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { promise, resolve, reject };
};

describe('ShipmentDetail - Skeleton de carga', () => {
  it('muestra skeletons mientras se cargan los datos y luego renderiza el detalle', async () => {
    const { enviosAPI } = await import('../../services/api');
    const d = deferred<{ data: any }>();
    (enviosAPI.getById as unknown as ReturnType<typeof vi.fn>).mockReturnValue(d.promise);

    const { container } = render(
      <MemoryRouter initialEntries={["/envios/1"]}>
        <Routes>
          <Route path="/envios/:id" element={<ShipmentDetail />} />
        </Routes>
      </MemoryRouter>
    );

    // Debe mostrar skeletons inicialmente
    expect(container.querySelector('.skeleton')).toBeInTheDocument();

    // Completar la carga
    d.resolve({
      data: {
        id: 1,
        numero_guia: 'ABC123',
        estado: 'pendiente',
        fecha_creacion: new Date().toISOString(),
      },
    });

    // Esperar a que aparezca el título con el número de guía
    const title = await screen.findByText(/Envío #ABC123/i);
    expect(title).toBeInTheDocument();

    // Ya no debería haber skeletons
    expect(container.querySelector('.skeleton')).not.toBeInTheDocument();
  });
});
