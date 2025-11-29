import { useState } from 'react';
import UploadBox from './components/UploadBox';
import { uploadImage, pollRoastCompletion } from './api';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [roastResult, setRoastResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileSelect = (selectedFile) => {
    setFile(selectedFile);
    setError(null);
    setRoastResult(null);
  };

  const handleRoast = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    setRoastResult(null);

    try {
      // Upload image
      const uploadResponse = await uploadImage(file);

      // Poll for completion
      const result = await pollRoastCompletion(uploadResponse.job_id);

      setRoastResult(result.result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setRoastResult(null);
    setError(null);
  };

  return (
    <div className="app">
      <div className="background-gradient"></div>

      <div className="container">
        <header className="header">
          <h1 className="title">
            🔥 Roast My Profile
          </h1>
          <p className="subtitle">
            AI-powered profile picture roasting • Brutally honest, hilariously accurate
          </p>
        </header>

        <main className="main-content">
          {!roastResult ? (
            <div className="upload-section">
              <UploadBox onFileSelect={handleFileSelect} />

              {file && !loading && (
                <button className="roast-button" onClick={handleRoast}>
                  <span className="button-icon">🔥</span>
                  Roast Me!
                </button>
              )}

              {loading && (
                <div className="loading-container">
                  <div className="loading-spinner"></div>
                  <p className="loading-text">Analyzing your questionable choices...</p>
                  <p className="loading-subtext">This might take a moment</p>
                </div>
              )}

              {error && (
                <div className="error-box">
                  <span className="error-icon">⚠️</span>
                  <p>{error}</p>
                </div>
              )}
            </div>
          ) : (
            <div className="result-section">
              <div className="roast-card">
                <div className="roast-header">
                  <h2>🔥 Your Roast</h2>
                </div>
                <div className="roast-content">
                  <p className="roast-text">{roastResult.roast}</p>
                </div>
              </div>

              <button className="reset-button" onClick={handleReset}>
                Try Another Picture
              </button>
            </div>
          )}
        </main>

        <footer className="footer">
          <p>Made with 🔥 and AI • All roasts are in good fun</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
