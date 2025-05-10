import { useState, useContext, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import '../assets/styles/Profile.css';

const Profile = () => {
  const { user, updateProfile } = useContext(AuthContext);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    full_name: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (user) {
      setFormData({
        username: user.username,
        email: user.email,
        full_name: user.full_name,
        password: '',
        confirmPassword: ''
      });
    }
  }, [user]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Check if password fields match if either is filled
    if ((formData.password || formData.confirmPassword) && formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    // Check password length if provided
    if (formData.password && formData.password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }

    setIsLoading(true);

    try {
      const updateData: any = {};
      
      // Only include fields that have changed
      if (formData.username !== user?.username) updateData.username = formData.username;
      if (formData.email !== user?.email) updateData.email = formData.email;
      if (formData.full_name !== user?.full_name) updateData.full_name = formData.full_name;
      if (formData.password) updateData.password = formData.password;

      // Only update if there are changes
      if (Object.keys(updateData).length > 0) {
        await updateProfile(updateData);
        setSuccess('Profile updated successfully');
      } else {
        setSuccess('No changes to save');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update profile');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="profile-page">
      <Navbar />
      <div className="container">
        <div className="profile-container">
          <div className="profile-form-container pixel-border">
            <h1 className="profile-title pixel-text">Your Profile</h1>
            {error && <div className="error-message">{error}</div>}
            {success && <div className="success-message">{success}</div>}
            <form onSubmit={handleSubmit} className="profile-form">
              <div className="form-group">
                <label htmlFor="username" className="form-label">Username</label>
                <input
                  type="text"
                  id="username"
                  name="username"
                  className="form-input"
                  value={formData.username}
                  onChange={handleChange}
                  required
                  minLength={3}
                  maxLength={50}
                />
              </div>
              <div className="form-group">
                <label htmlFor="email" className="form-label">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  className="form-input"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="full_name" className="form-label">Full Name</label>
                <input
                  type="text"
                  id="full_name"
                  name="full_name"
                  className="form-input"
                  value={formData.full_name}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="password" className="form-label">New Password (leave blank to keep current)</label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  className="form-input"
                  value={formData.password}
                  onChange={handleChange}
                  minLength={8}
                />
              </div>
              <div className="form-group">
                <label htmlFor="confirmPassword" className="form-label">Confirm New Password</label>
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  className="form-input"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  minLength={8}
                />
              </div>
              <button 
                type="submit" 
                className="btn btn-primary profile-submit" 
                disabled={isLoading}
              >
                {isLoading ? 'Saving...' : 'Save Changes'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
