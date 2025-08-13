import React from 'react';
import SimpleAdvancedForm from '../components/SimpleAdvancedForm';
// 🇨🇺 Estilos cargados globalmente desde main.tsx

const SimpleAdvancedPage: React.FC = () => {
  return (
    <div className="simple-page-container">
      <SimpleAdvancedForm />
    </div>
  );
};

export default SimpleAdvancedPage;
