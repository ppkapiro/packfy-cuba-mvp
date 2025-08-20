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
    <div className="pagination-container">
      {totalItems && itemsPerPage && (
        <div className="pagination-info">
          Mostrando {Math.min((currentPage - 1) * itemsPerPage + 1, totalItems)} 
          - {Math.min(currentPage * itemsPerPage, totalItems)} 
          de {totalItems} resultados
        </div>
      )}
      
      <ul className="pagination">
        {/* Botón Primera página */}
        <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
          <button
            onClick={() => onPageChange(1)}
            disabled={currentPage === 1}
            className="page-link"
            aria-label="Primera página"
          >
            &laquo;
          </button>
        </li>
        
        {/* Botón Anterior */}
        <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
          <button
            onClick={() => onPageChange(currentPage - 1)}
            disabled={currentPage === 1}
            className="page-link"
            aria-label="Página anterior"
          >
            &lsaquo;
          </button>
        </li>
        
        {/* Números de página */}
        {getPageNumbers().map(page => (
          <li key={page} className={`page-item ${page === currentPage ? 'active' : ''}`}>
            <button
              onClick={() => onPageChange(page)}
              className="page-link"
            >
              {page}
            </button>
          </li>
        ))}
        
        {/* Botón Siguiente */}
        <li className={`page-item ${currentPage === totalPages ? 'disabled' : ''}`}>
          <button
            onClick={() => onPageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
            className="page-link"
            aria-label="Página siguiente"
          >
            &rsaquo;
          </button>
        </li>
        
        {/* Botón Última página */}
        <li className={`page-item ${currentPage === totalPages ? 'disabled' : ''}`}>
          <button
            onClick={() => onPageChange(totalPages)}
            disabled={currentPage === totalPages}
            className="page-link"
            aria-label="Última página"
          >
            &raquo;
          </button>
        </li>
      </ul>
    </div>
  );
};

export default Pagination;
