import React from 'react';
import {
  Skeleton,
  CardSkeleton,
  TableRowSkeleton,
  ActivityFeedSkeleton,
  ChartSkeleton,
  FullPageDashboardSkeleton,
  SimulatorSkeleton,
} from '../ui/Skeleton';

interface LoadingStateProps {
  type?: 'card' | 'chart' | 'table' | 'timeline' | 'fullPage' | 'simulator';
  count?: number;
}

export const LoadingState: React.FC<LoadingStateProps> = ({ type = 'card', count = 1 }) => {
  if (type === 'fullPage') {
    return <FullPageDashboardSkeleton />;
  }

  if (type === 'simulator') {
    return <SimulatorSkeleton />;
  }

  if (type === 'table') {
    return <TableRowSkeleton rows={count || 5} />;
  }

  if (type === 'chart') {
    return <ChartSkeleton />;
  }

  if (type === 'timeline') {
    return <ActivityFeedSkeleton count={count || 5} />;
  }

  // Default card grid loader
  return <CardSkeleton count={count || 4} />;
};

export default LoadingState;

