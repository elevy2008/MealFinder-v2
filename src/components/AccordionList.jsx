import React, { useState } from 'react';
import LocationCard from './LocationCard';

const AccordionList = ({ locations, isLoading, onViewMap }) => {
  const [isExpanded, setIsExpanded] = useState(true);

  const accordionStyle = {
    width: '100%',
    backgroundColor: 'white',
    borderRadius: '8px',
    overflow: 'hidden',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    transition: 'margin 0.3s ease',
  };

  const contentStyle = {
    maxHeight: isExpanded ? 'calc(100vh - 200px)' : '0',
    overflow: 'hidden',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    overflowY: isExpanded ? 'auto' : 'hidden',
    WebkitOverflowScrolling: 'touch',
    position: 'relative',
    zIndex: 1,
    transform: isExpanded ? 'translateY(0)' : 'translateY(-10px)',
    opacity: isExpanded ? 1 : 0,
  };

  const contentContainerStyle = {
    padding: isExpanded ? '10px' : '0 10px',
    transition: 'padding 0.3s ease',
  };

  return (
    <div
      style={accordionStyle}
      role="region"
      aria-label="Food truck locations list"
    >
      <div
        onClick={() => setIsExpanded(!isExpanded)}
        role="button"
        aria-expanded={isExpanded}
        tabIndex={0}
        style={{
          padding: '15px',
          backgroundColor: '#f8f9fa',
          cursor: 'pointer',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          borderBottom: isExpanded ? '1px solid #dee2e6' : 'none',
        }}
      >
        <h2 style={{ margin: 0, fontSize: '1.25rem', color: '#212529' }}>Food Truck Locations</h2>
        <span style={{
          transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)',
          transition: 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          fontSize: '20px',
          color: '#495057',
        }} aria-hidden="true">▼</span>
      </div>
      <div style={contentStyle}>
        <div style={contentContainerStyle}>
          {isLoading ? (
            <p style={{ textAlign: 'center', padding: '20px' }}>Loading locations...</p>
          ) : (
            locations.map((location, index) => (
              <LocationCard
                key={index}
                location={location}
                distance={location.distance.toFixed(1)}
                duration={Math.round(location.distance / 3.1 * 60) + 8}
                isClose={location.isClose}
                onViewMap={onViewMap}
              />
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default AccordionList;