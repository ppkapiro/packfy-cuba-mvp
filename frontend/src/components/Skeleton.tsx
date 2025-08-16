import React from 'react';

type CSSSize = string | number;

export interface SkeletonProps {
  width?: CSSSize;
  height?: CSSSize;
  rounded?: boolean;
  className?: string;
}

export const Skeleton: React.FC<SkeletonProps> = ({ width = '100%', height = 12, rounded = false, className = '' }) => {
  // Mapear tamaños comunes a clases CSS
  const getHeightClass = (h: CSSSize): string => {
    if (typeof h === 'number') {
      if (h <= 8) return 'skeleton-h-8';
      if (h <= 10) return 'skeleton-h-10';
      if (h <= 12) return 'skeleton-h-12';
      if (h <= 14) return 'skeleton-h-14';
      if (h <= 16) return 'skeleton-h-16';
      if (h <= 20) return 'skeleton-h-20';
      if (h <= 24) return 'skeleton-h-24';
    }
    return 'skeleton-h-12'; // default
  };

  const getWidthClass = (w: CSSSize): string => {
    if (w === '25%') return 'skeleton-w-25';
    if (w === '50%') return 'skeleton-w-50';
    if (w === '75%') return 'skeleton-w-75';
    if (w === '80%') return 'skeleton-w-80';
    if (w === '100%') return 'skeleton-w-full';
    return 'skeleton-w-full'; // default
  };

  const heightClass = getHeightClass(height);
  const widthClass = getWidthClass(width);
  const roundedClass = rounded ? 'skeleton-rounded' : '';

  return (
    <div
      className={`skeleton ${heightClass} ${widthClass} ${roundedClass} ${className}`}
    />
  );
};

export const SkeletonText: React.FC<{ lines?: number; gap?: number; className?: string }> = ({
  lines = 3,
  gap = 10,
  className = ''
}) => {
  // Mapear gaps a clases CSS predefinidas
  const getGapClass = (gapValue: number): string => {
    if (gapValue <= 5) return 'skeleton-gap-5';
    if (gapValue <= 10) return 'skeleton-gap-10';
    if (gapValue <= 15) return 'skeleton-gap-15';
    if (gapValue <= 20) return 'skeleton-gap-20';
    return 'skeleton-gap-10'; // default
  };

  const gapClass = getGapClass(gap);

  return (
    <div className={`skeleton-text-container ${gapClass} ${className}`}>
      {Array.from({ length: lines }).map((_, i) => (
        <Skeleton
          key={i}
          height={12}
          className="skeleton-text-line"
        />
      ))}
    </div>
  );
};

export const SkeletonRow: React.FC<{ columns?: number; className?: string }> = ({
  columns = 4,
  className = ''
}) => {
  const gridClass = `skeleton-row-grid skeleton-row-grid-${Math.min(columns, 5)}`;

  return (
    <div className={`${gridClass} ${className}`}>
      {Array.from({ length: columns }).map((_, i) => (
        <Skeleton key={i} height={14} />
      ))}
    </div>
  );
};

export default Skeleton;
