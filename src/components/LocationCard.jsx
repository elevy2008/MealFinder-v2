import React from 'react';

const LocationCard = ({ location, distance, duration, isClose, onViewMap }) => {
  const cardStyle = {
    padding: '15px',
    borderBottom: '1px solid #eee',
    cursor: 'pointer',
    backgroundColor: 'white',
    borderLeft: isClose ? '3px solid #00ff00' : 'none',
    boxShadow: isClose ? '0 0 10px rgba(0, 255, 0, 0.3)' : 'none',
  };

  return (
    <div style={cardStyle} className="location-card">
      <h3>{location.Location}</h3>
      <p>Time: {location.Time}</p>
      <p>Route: {location.Route}</p>
      <p>Distance: {distance} miles</p>
      <p>Walking time: ~{duration} minutes (includes 8-minute buffer)</p>
      <button 
        className="view-map-btn"
        onClick={() => onViewMap(location)}
      >
        View on Map
      </button>
    </div>
  );
};

export default LocationCard;