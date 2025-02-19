import React from 'react';

const HamburgerMenu = ({ onClick, isOpen }) => {
  const style = {
    position: 'absolute',
    top: '20px',
    left: '20px',
    zIndex: 1000,
    background: 'white',
    bordercolor: 'black',
    padding: '10px',
    borderRadius: '4px',
    cursor: 'pointer',
    boxShadow: '0 2px 6px rgba(0, 0, 0, 0.1)',
    border: 'none',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    width: '40px',
    height: '40px',
    bordercolor: 'black',

  };

  
  
  return (
    <button 
      style={style} 
      onClick={onClick} 
      aria-label="Toggle menu"
      aria-expanded={isOpen}
    >
      ☰
    </button>
  );
};


export default HamburgerMenu;