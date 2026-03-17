import { PerformanceGrade as Grade } from '@/types/contractor';

interface PerformanceGradeProps {
  grade: Grade;
  size?: 'sm' | 'md' | 'lg';
}

const gradeConfig: Record<Grade, { bg: string; text: string; label: string }> = {
  A: { bg: 'bg-green-100', text: 'text-green-800', label: 'Excellent' },
  B: { bg: 'bg-blue-100', text: 'text-blue-800', label: 'Good' },
  C: { bg: 'bg-yellow-100', text: 'text-yellow-800', label: 'Average' },
  D: { bg: 'bg-orange-100', text: 'text-orange-800', label: 'Poor' },
  F: { bg: 'bg-red-100', text: 'text-red-800', label: 'Failing' },
};

const sizeClasses = {
  sm: 'w-7 h-7 text-sm',
  md: 'w-9 h-9 text-lg',
  lg: 'w-12 h-12 text-2xl',
};

export function PerformanceGrade({ grade, size = 'md' }: PerformanceGradeProps) {
  const config = gradeConfig[grade];

  return (
    <div className="flex flex-col items-center gap-0.5">
      <div
        className={`${sizeClasses[size]} rounded-full ${config.bg} ${config.text} font-bold flex items-center justify-center`}
        title={`Grade ${grade}: ${config.label}`}
      >
        {grade}
      </div>
      {size !== 'sm' && (
        <span className={`text-xs ${config.text}`}>{config.label}</span>
      )}
    </div>
  );
}
