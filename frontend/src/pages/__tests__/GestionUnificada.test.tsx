import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import GestionUnificada from '../GestionUnificada';
import { vi } from 'vitest';

vi.mock('../../services/api', () => ({
  enviosAPI: {
    getAll: vi.fn(),
    delete: vi.fn(),
  },
}));

const deferred = <T,>() => {
  let resolve!: (v: T) => void;
  let reject!: (e: any) => void;
  const promise = new Promise<T>((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { promise, resolve, reject };
};

describe('GestionUnificada - Skeleton de carga', () => {
  it('muestra skeletons mientras se cargan los envíos y luego la tabla', async () => {
    const { enviosAPI } = await import('../../services/api');
    const d = deferred<{ data: any }>();
    (enviosAPI.getAll as unknown as ReturnType<typeof vi.fn>).mockReturnValue(d.promise);

    const { container, findByText } = render(<GestionUnificada />);

    // Debe mostrar skeletons inicialmente
    expect(container.querySelector('.skeleton')).toBeInTheDocument();

    // Completar la carga
    d.resolve({ data: [] });

    // Esperar a que muestre el estado vacío
    const empty = await findByText(/No hay envíos registrados|No se encontraron envíos/i);
    expect(empty).toBeInTheDocument();

    // Ya no debería haber skeletons
    expect(container.querySelector('.skeleton')).not.toBeInTheDocument();
  });
});
