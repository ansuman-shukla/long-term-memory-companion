import '../assets/styles/LoadingSpinner.css';

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large';
  color?: 'primary' | 'secondary' | 'white';
}

const LoadingSpinner = ({ size = 'medium', color = 'primary' }: LoadingSpinnerProps) => {
  return (
    <div className={`spinner-container spinner-${size}`}>
      <div className={`pixel-spinner spinner-${color}`}>
        <div className="pixel-1"></div>
        <div className="pixel-2"></div>
        <div className="pixel-3"></div>
        <div className="pixel-4"></div>
      </div>
    </div>
  );
};

export default LoadingSpinner;
