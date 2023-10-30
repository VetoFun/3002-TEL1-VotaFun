import styles from './styles/dots.module.css';

const LoadingDots = () => {
  return (
    <div className="inline-flex gap-1">
      <div
        className={`h-1 w-1 animate-bounce rounded-full bg-accent-content ${styles['dot-1']}`}
        data-testid="loading-dot"
      ></div>
      <div
        className={`h-1 w-1 animate-bounce rounded-full bg-accent-content ${styles['dot-2']}`}
        data-testid="loading-dot"
      ></div>
      <div
        className={`h-1 w-1 animate-bounce rounded-full bg-accent-content ${styles['dot-3']}`}
        data-testid="loading-dot"
      ></div>
    </div>
  );
};

export { LoadingDots };
