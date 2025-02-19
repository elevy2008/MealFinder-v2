import React, { useState } from 'react';
import LocationCard from './LocationCard';

const AccordionList = ({ locations, isLoading, onViewMap }) => {
  // State to track if the accordion is expanded or collapsed
  const [isExpanded, setIsExpanded] = useState(true);

  // CSS styles for the accordion container
  const accordionStyle = {
    width: '100%',
    backgroundColor: 'white',
    borderRadius: '8px',
    overflow: 'hidden',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    transition: 'margin 0.3s ease',
  };

  // CSS styles for the accordion header
  const headerStyle = {
    padding: '15px',
    backgroundColor: '#f8f9fa',
    cursor: 'pointer',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottom: isExpanded ? '1px solid #dee2e6' : 'none',
    userSelect: 'none',
    transition: 'all 0.3s ease',
    position: 'relative',
    zIndex: 2,
    ':hover': {
      backgroundColor: '#e9ecef',
    },
  };

  // CSS styles for the accordion content area
  const contentStyle = {
    maxHeight: isExpanded ? 'calc(100vh - 200px)' : '0', // Adjust max height based on expanded state
    overflow: 'hidden',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    overflowY: isExpanded ? 'auto' : 'hidden', // Scroll only if expanded
    WebkitOverflowScrolling: 'touch', // Smooth scrolling for mobile devices
    position: 'relative',
    zIndex: 1,
    transform: isExpanded ? 'translateY(0)' : 'translateY(-10px)', // Add a subtle transform animation
    opacity: isExpanded ? 1 : 0, // Fade in/out effect
  };

  // CSS styles for the arrow indicating the accordion state
  const arrowStyle = {
    transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)', // Rotate arrow depending on the accordion state
    transition: 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    fontSize: '20px',
    color: '#495057',
  };

  // CSS styles for the content container
  const contentContainerStyle = {
    padding: isExpanded ? '10px' : '0 10px', // Adjust padding based on expanded state
    transition: 'padding 0.3s ease',
  };

  return (
    <div
      style={accordionStyle}
      data-testid="accordion-container" // Test identifier for automated tests
      role="region" // Accessibility role for screen readers
      aria-label="Food truck locations list" // Description for accessibility tools
    >
      <div
        style={headerStyle}
        onClick={() => {
          // Toggle accordion expanded/collapsed state on header click
          setIsExpanded(!isExpanded);
          console.log('Accordion state changed:', !isExpanded ? 'expanded' : 'collapsed');
        }}
        role="button" // Accessibility role indicating this is a clickable element
        aria-expanded={isExpanded} // Indicates whether the accordion is expanded
        tabIndex={0} // Allows keyboard focus for accessibility
      >
        <h2 style={{ margin: 0, fontSize: '1.25rem', color: '#212529' }}>Food Truck Locations</h2>
        <span style={arrowStyle} aria-hidden="true">▼</span> {/* Arrow icon */}
      </div>
      <div style={contentStyle}>
        <div style={contentContainerStyle}>
          {isLoading ? (
            // Display a loading message while locations are being fetched
            <p style={{ textAlign: 'center', padding: '20px' }}>Loading locations...</p>
          ) : (
            // Map over the locations and render a LocationCard for each
            locations.map((location, index) => (
              <LocationCard
                key={index} // Unique key for React rendering optimization
                location={location} // Pass location details to the card
                distance={location.distance.toFixed(2)+2} // Format distance to 2 decimal places
                duration={Math.round(location.distance / 3.1 * 60)+5} // Calculate walking time based on distance
                isClose={location.isClose} // Indicate whether this location is close to the user
                onViewMap={onViewMap} // Function to handle map view actions
              />
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default AccordionList;