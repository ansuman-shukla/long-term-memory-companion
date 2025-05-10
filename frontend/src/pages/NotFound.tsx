import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';

const NotFound = () => {
  return (
    <div className="not-found-page">
      <Navbar />
      <div className="container text-center" style={{ marginTop: '5rem' }}>
        <div className="pixel-border" style={{ padding: '2rem', maxWidth: '500px', margin: '0 auto' }}>
          <h1 className="pixel-text" style={{ color: 'var(--color-primary)' }}>404</h1>
          <h2 className="mb-3">Page Not Found</h2>
          <p className="mb-4">The page you are looking for doesn't exist or has been moved.</p>
          <Link to="/" className="btn btn-primary">Go Home</Link>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
