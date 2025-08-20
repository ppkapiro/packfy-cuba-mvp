import { useTenant } from '../contexts/TenantContext';

const TenantDebug = () => {
  const {
    empresaActual,
    empresasDisponibles,
    isLoading,
    perfilActual
  } = useTenant();

  return (
    <div style={{
      position: 'fixed',
      top: '10px',
      right: '10px',
      background: 'white',
      border: '2px solid red',
      padding: '10px',
      zIndex: 9999,
      fontSize: '12px',
      maxWidth: '300px'
    }}>
      <h3>🐛 TENANT DEBUG</h3>
      <p><strong>isLoading:</strong> {isLoading ? 'true' : 'false'}</p>
      <p><strong>empresasDisponibles:</strong> {empresasDisponibles.length}</p>
      <p><strong>empresaActual:</strong> {empresaActual?.nombre || 'null'}</p>
      <p><strong>perfilActual:</strong> {perfilActual?.rol || 'null'}</p>

      <details>
        <summary>Empresas ({empresasDisponibles.length})</summary>
        <pre>{JSON.stringify(empresasDisponibles, null, 2)}</pre>
      </details>
    </div>
  );
};

export default TenantDebug;
