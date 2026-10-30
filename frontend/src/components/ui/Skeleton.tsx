import React from 'react';

// ----------------------------------------------------------------------
// 1. Base Skeleton Component
// ----------------------------------------------------------------------
export interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string;
}

export const Skeleton: React.FC<SkeletonProps> = ({ className = '', ...props }) => {
  return (
    <div
      className={`bg-gray-700/70 dark:bg-slate-800/80 animate-pulse rounded-md ${className}`}
      {...props}
    />
  );
};

// ----------------------------------------------------------------------
// 2. CardSkeleton Variant (for Dashboard Stats Cards)
// ----------------------------------------------------------------------
export interface CardSkeletonProps {
  count?: number;
  className?: string;
}

export const CardSkeleton: React.FC<CardSkeletonProps> = ({ count = 4, className = '' }) => {
  return (
    <div className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 w-full ${className}`}>
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="h-32 rounded-2xl bg-slate-900/80 border border-slate-800/80 p-5 flex flex-col justify-between shadow-lg"
        >
          <div className="flex items-center justify-between">
            <Skeleton className="h-4 w-28" />
            <Skeleton className="h-9 w-9 rounded-xl" />
          </div>
          <div className="space-y-2">
            <Skeleton className="h-7 w-20" />
            <Skeleton className="h-3 w-36" />
          </div>
        </div>
      ))}
    </div>
  );
};

// ----------------------------------------------------------------------
// 3. TableRowSkeleton Variant (for Incidents Table)
// ----------------------------------------------------------------------
export interface TableRowSkeletonProps {
  rows?: number;
  className?: string;
}

export const TableRowSkeleton: React.FC<TableRowSkeletonProps> = ({ rows = 5, className = '' }) => {
  return (
    <div className={`rounded-2xl border border-slate-800 bg-slate-900/60 overflow-hidden shadow-xl ${className}`}>
      <div className="p-4 border-b border-slate-800 bg-slate-950/40 flex items-center justify-between">
        <Skeleton className="h-4 w-48" />
        <Skeleton className="h-3 w-24" />
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b border-slate-800 bg-slate-950/60">
              <th className="p-3.5 pl-5"><Skeleton className="h-3 w-20" /></th>
              <th className="p-3.5"><Skeleton className="h-3 w-16" /></th>
              <th className="p-3.5"><Skeleton className="h-3 w-24" /></th>
              <th className="p-3.5"><Skeleton className="h-3 w-32" /></th>
              <th className="p-3.5"><Skeleton className="h-3 w-20" /></th>
              <th className="p-3.5"><Skeleton className="h-3 w-20" /></th>
              <th className="p-3.5"><Skeleton className="h-3 w-16" /></th>
              <th className="p-3.5 pr-5 text-right"><Skeleton className="h-3 w-16 ml-auto" /></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {Array.from({ length: rows }).map((_, i) => (
              <tr key={i} className="bg-slate-950/30">
                <td className="p-3.5 pl-5"><Skeleton className="h-4 w-20" /></td>
                <td className="p-3.5"><Skeleton className="h-3 w-16" /></td>
                <td className="p-3.5"><Skeleton className="h-4 w-28" /></td>
                <td className="p-3.5"><Skeleton className="h-3 w-36" /></td>
                <td className="p-3.5"><Skeleton className="h-5 w-20 rounded-full" /></td>
                <td className="p-3.5"><Skeleton className="h-4 w-12" /></td>
                <td className="p-3.5"><Skeleton className="h-5 w-20 rounded-full" /></td>
                <td className="p-3.5 pr-5 text-right"><Skeleton className="h-7 w-16 rounded-lg ml-auto" /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// ----------------------------------------------------------------------
// 4. ActivityFeedSkeleton Variant (for SOC Activity Feed)
// ----------------------------------------------------------------------
export interface ActivityFeedSkeletonProps {
  count?: number;
  className?: string;
}

export const ActivityFeedSkeleton: React.FC<ActivityFeedSkeletonProps> = ({ count = 5, className = '' }) => {
  return (
    <div className={`rounded-2xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur-xl shadow-lg flex flex-col h-full ${className}`}>
      <div className="flex items-center justify-between mb-6">
        <Skeleton className="h-5 w-44" />
        <Skeleton className="h-3 w-3 rounded-full" />
      </div>

      <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-800">
        {Array.from({ length: count }).map((_, i) => (
          <div key={i} className="relative">
            <div className="absolute -left-[31px] top-0 flex items-center justify-center w-6 h-6 rounded-full bg-slate-950 border border-slate-800">
              <Skeleton className="w-3 h-3 rounded-full" />
            </div>

            <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-2">
              <div className="flex items-center justify-between">
                <Skeleton className="h-3.5 w-3/4" />
                <Skeleton className="h-3 w-12" />
              </div>
              <div className="flex items-center space-x-2">
                <Skeleton className="w-1.5 h-1.5 rounded-full" />
                <Skeleton className="h-2.5 w-24" />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// ----------------------------------------------------------------------
// 5. ChartSkeleton Variant (for Threat Trend & Distribution Charts)
// ----------------------------------------------------------------------
export interface ChartSkeletonProps {
  className?: string;
  height?: string;
}

export const ChartSkeleton: React.FC<ChartSkeletonProps> = ({ className = '', height = 'h-80' }) => {
  return (
    <div className={`w-full rounded-2xl border border-slate-800 bg-slate-900/80 p-5 flex flex-col justify-between shadow-xl ${height} ${className}`}>
      <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
        <Skeleton className="h-4 w-40" />
        <Skeleton className="h-3 w-20" />
      </div>
      <div className="flex-1 w-full bg-slate-950/60 rounded-xl border border-slate-800/60 p-4 flex items-end justify-between gap-2">
        <Skeleton className="h-1/3 flex-1 rounded-t-md" />
        <Skeleton className="h-2/3 flex-1 rounded-t-md" />
        <Skeleton className="h-1/2 flex-1 rounded-t-md" />
        <Skeleton className="h-3/4 flex-1 rounded-t-md" />
        <Skeleton className="h-2/5 flex-1 rounded-t-md" />
        <Skeleton className="h-4/5 flex-1 rounded-t-md" />
      </div>
    </div>
  );
};

// ----------------------------------------------------------------------
// 6. FullPageDashboardSkeleton Variant (for Executive SOC Dashboard layout)
// ----------------------------------------------------------------------
export const FullPageDashboardSkeleton: React.FC = () => {
  return (
    <div className="space-y-6 animate-pulse">
      {/* Top Banner Skeleton */}
      <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 flex justify-between items-center h-24">
        <div className="space-y-2">
          <Skeleton className="h-6 w-64" />
          <Skeleton className="h-4 w-96" />
        </div>
        <Skeleton className="h-10 w-36 rounded-xl" />
      </div>

      {/* Stats Cards Grid Skeleton */}
      <CardSkeleton count={4} />

      {/* Main Charts & Activity Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <ChartSkeleton height="h-72" />
          <TableRowSkeleton rows={4} />
        </div>
        <div className="lg:col-span-1">
          <ActivityFeedSkeleton count={5} />
        </div>
      </div>
    </div>
  );
};

// ----------------------------------------------------------------------
// 7. SimulatorSkeleton Variant (for Phishing Simulation Lab layout)
// ----------------------------------------------------------------------
export const SimulatorSkeleton: React.FC = () => {
  return (
    <div className="space-y-6 animate-pulse">
      {/* Header Banner Skeleton */}
      <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 flex justify-between items-center h-24">
        <div className="space-y-2">
          <Skeleton className="h-6 w-72" />
          <Skeleton className="h-4 w-80" />
        </div>
        <Skeleton className="h-9 w-32 rounded-xl" />
      </div>

      {/* Filter bar skeleton */}
      <div className="h-14 rounded-2xl bg-slate-900/60 border border-slate-800 p-3 flex gap-3 items-center">
        <Skeleton className="h-8 w-40 rounded-xl" />
        <Skeleton className="h-8 w-32 rounded-xl" />
        <Skeleton className="h-8 flex-1 rounded-xl" />
      </div>

      {/* Scenario cards grid skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="h-56 rounded-2xl bg-slate-900/80 border border-slate-800 p-5 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <Skeleton className="h-4 w-24 rounded-full" />
                <Skeleton className="h-4 w-16" />
              </div>
              <Skeleton className="h-5 w-4/5" />
              <Skeleton className="h-3 w-full" />
              <Skeleton className="h-3 w-2/3" />
            </div>
            <Skeleton className="h-9 w-full rounded-xl" />
          </div>
        ))}
      </div>
    </div>
  );
};

// ----------------------------------------------------------------------
// 8. LoadingWrapper Component (Smooth Transition Wrapper)
// ----------------------------------------------------------------------
export interface LoadingWrapperProps {
  isLoading: boolean;
  fallback?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
}

export const LoadingWrapper: React.FC<LoadingWrapperProps> = ({
  isLoading,
  fallback = <CardSkeleton />,
  children,
  className = '',
}) => {
  if (isLoading) {
    return <div className={`transition-opacity duration-300 ${className}`}>{fallback}</div>;
  }

  return (
    <div className={`transition-opacity duration-300 animate-in fade-in duration-500 ${className}`}>
      {children}
    </div>
  );
};

export default Skeleton;

