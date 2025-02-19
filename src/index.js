import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './styles.css';
import Modal from 'react-modal';
import GeolocationErrorBoundary from './components/GeolocationErrorBoundary';

// Initialize ReactModal
Modal.setAppElement('#root');

const root = createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <GeolocationErrorBoundary>
      <App />
    </GeolocationErrorBoundary>
  </React.StrictMode>
);