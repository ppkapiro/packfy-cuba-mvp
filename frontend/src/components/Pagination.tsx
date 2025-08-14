import React from 'react';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  totalItems?: number;
  itemsPerPage?: number;
}

const Pagination: React.FC<PaginationProps> = ({
  currentPage,
  totalPages,
  onPageChange,
  totalItems,
  itemsPerPage
}) => {
  // Generar un array de números de página para mostrar
  const getPageNumbers = () => {
    const pages = [];

    // Mostrar como máximo 5 páginas alrededor de la página actual
    const maxPagesToShow = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxPagesToShow / 2));
    let endPage = Math.min(totalPages, startPage + maxPagesToShow - 1);

    // Ajustar startPage si estamos en las últimas páginas
    if (endPage - startPage + 1 < maxPagesToShow) {
      startPage = Math.max(1, endPage - maxPagesToShow + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }

    return pages;
  };

  if (totalPages <= 1) return null;

  return (
    <div className="packfy-pagination">
      {/* Información de resultados */}
      <div className="pagination-info">
        <span className="results-text">
          📊 Mostrando <strong>{Math.min((currentPage - 1) * itemsPerPage! + 1, totalItems!)}</strong> a <strong>{Math.min(currentPage * itemsPerPage!, totalItems!)}</strong> de <strong>{totalItems}</strong> envíos
        </span>
      </div>

      {/* Controles de paginación */}
      <div className="pagination-controls">
        {/* Botón Primera página */}
        <button
          onClick={() => onPageChange(1)}
          disabled={currentPage === 1}
          className={`page-btn page-first ${currentPage === 1 ? 'disabled' : ''}`}
          title="Primera página"
        >
          ⏪
        </button>

        {/* Botón Anterior */}
        <button
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          className={`page-btn page-prev ${currentPage === 1 ? 'disabled' : ''}`}
          title="Página anterior"
        >
          ⬅️
        </button>

        {/* Números de página */}
        <div className="page-numbers">
          {getPageNumbers().map(page => (
            <button
              key={page}
              onClick={() => onPageChange(page)}
              className={`page-btn page-number ${page === currentPage ? 'active' : ''}`}
            >
              {page}
            </button>
          ))}
        </div>

        {/* Botón Siguiente */}
        <button
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          className={`page-btn page-next ${currentPage === totalPages ? 'disabled' : ''}`}
          title="Página siguiente"
        >
          ➡️
        </button>

        {/* Botón Última página */}
        <button
          onClick={() => onPageChange(totalPages)}
          disabled={currentPage === totalPages}
          className={`page-btn page-last ${currentPage === totalPages ? 'disabled' : ''}`}
          title="Última página"
        >
          ⏩
        </button>
      </div>

      {/* Información adicional */}
      <div className="pagination-summary">
        <span className="page-summary">
          Página <strong>{currentPage}</strong> de <strong>{totalPages}</strong>
        </span>
      </div>
    </div>
  );
};

export default Pagination;
