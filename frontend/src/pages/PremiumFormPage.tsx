import React from 'react';
import PremiumCompleteForm from '../components/PremiumCompleteForm';
// 🇨🇺 Estilos cargados globalmente desde main.tsx

const PremiumFormPage: React.FC = () => {
  return (
    <div className="premium-page-container">
      <PremiumCompleteForm />
    </div>
  );
};

export default PremiumFormPage;
