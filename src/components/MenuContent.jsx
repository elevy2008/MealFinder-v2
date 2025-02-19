import React, { useState } from 'react';
import * as Dialog from '@radix-ui/react-dialog';

const MenuContent = ({ isOpen, onClose }) => {
  const [modalOpen, setModalOpen] = useState(false);
  const [modalTitle, setModalTitle] = useState("");
  const [modalContent, setModalContent] = useState("");

  if (!isOpen) return null;

  const handleItemClick = (title, content) => {
    setModalTitle(title);  // Set correct title for each popup
    setModalContent(content);
    setModalOpen(true);
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      width: '250px',
      height: '100vh',
      backgroundColor: 'white',
      boxShadow: '2px 0 5px rgba(0, 0, 0, 0.1)',
      padding: '20px',
      transform: isOpen ? 'translateX(0)' : 'translateX(-100%)',
      transition: 'transform 0.3s ease-in-out',
      zIndex: 999
    }}>
      <h2 style={{ marginTop: '60px', marginBottom: '20px' }}>MealFinder</h2>      

      {/* Ethan Levy Popup Trigger */}
      <div 
        style={{ padding: '10px 0', borderBottom: '1px solid #eee', cursor: 'pointer' }} 
        onClick={() => handleItemClick("Ethan Levy", "I am a NYC High School Student trying to make a change via technology. I am a self-taught programmer and entrepreneur who is here to help. If you have any questions or want to reach out, you can contact me at: ethanjonathanlevy@gmail.com")}
      >
        <h3 style={{ marginBottom: '10px' }}>By Ethan Levy</h3>
      </div>

      {/* Other Menu Items */}
      <div 
        style={{ padding: '10px 0', borderBottom: '1px solid #eee', cursor: 'pointer' }} 
        onClick={() => handleItemClick("About", "The idea originated while volunteering at the Coalition for the Homeless's Grand Central Food Program, where several food trucks provided meals to those in need. One evening, while distributing sandwiches from a food truck, we ran out of food with over 50 individuals still waiting in line. Many remained in the same spot throughout the night, unaware of the locations of other food trucks in the city––they went to sleep hungry. This experience inspired the creation of MealFinder, a web app that provides real-time information on the locations of food trucks in New York City.")}>
        About
      </div>

      {/* FAQs with full content */}
      <div 
        style={{ padding: '10px 0', borderBottom: '1px solid #eee', cursor: 'pointer' }} 
        onClick={() => handleItemClick("FAQs", 
        `**Frequently Asked Questions:**
        
1. **How does this app work?** 
   This app helps you find nearby food trucks based on your location. It shows their routes, schedules, and provides directions on when to leave to arrive on time.
   
2. **How do you get food truck data?** 
   We use publicly available schedules from food truck vendors and city databases. The data is regularly updated to ensure accuracy.
   
3. **Why is my location incorrect?** 
   If your location appears inaccurate, make sure location services are enabled in your browser or device settings. You can also refresh the page to update your location.
   
4. **How do I know when to leave for a food truck?** 
   Each food truck listing calculates the **best time to leave** based on your distance, estimated walking time, and an **8-minute buffer** to ensure you arrive on time.
   
5. **Can I see the food truck locations on a map?** 
   Yes! Clicking on a food truck will show its location on the map, along with details such as arrival time, route, and distance from your current location.
   
6. **What if I can’t find a food truck near me?** 
   If no food trucks appear, it might be because:
   - Food trucks in your area have no scheduled stops today.
   - Your location services are turned off.
   - The database is being updated. Try refreshing the page later.
   
7. **How often is the data updated?** 
   We update food truck schedules daily to provide the most accurate information.
   
8. **Can I favorite or save locations?** 
   Currently, we don’t have a "favorites" feature, but we are working on adding it in future updates.
   
9. **Who built this app?** 
   This app was created by Ethan Levy to make it easier for users to find food trucks in their city.
   
10. **How can I contact support?** 
    If you have any issues or suggestions, you can contact us at ethanjonathanlevy@gmail.com.`)}>
        FAQs
      </div>

      <div 
        style={{ padding: '10px 0', borderBottom: '1px solid #eee', cursor: 'pointer' }} 
        onClick={() => handleItemClick("Contact", "Contact us at: ethanjonathanlevy@gmail.com")}>
        Contact
      </div>

      {/* Close Menu Button */}
      <button 
        onClick={onClose}
        style={{
          position: 'absolute',
          bottom: '65px',
          left: '75px',
          padding: '10px 20px',
          backgroundColor: '#4285F4',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer'
        }}
      >
        Close Menu
      </button>

      {/* Popup Dialog - Now with Scrollable FAQ Support */}
      {modalOpen && (
        <Dialog.Root open={modalOpen} onOpenChange={setModalOpen}>
          <Dialog.Portal>
            <Dialog.Overlay style={{
              backgroundColor: 'rgba(0, 0, 0, 0.5)',
              position: 'fixed',
              inset: 0,
              zIndex: 1000
            }} />
            <Dialog.Content style={{
              position: 'fixed',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              backgroundColor: 'white',
              padding: '20px',
              borderRadius: '8px',
              width: '400px', // Increased width
              maxHeight: '500px', // Ensures content fits
              textAlign: 'left',
              boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)',
              zIndex: 1001,
              overflowY: 'auto' // Enables scrolling for long content
            }}>
              <Dialog.Title>{modalTitle}</Dialog.Title>
              <p style={{ whiteSpace: 'pre-line' }}>{modalContent}</p> {/* Ensures FAQ formatting */}
              <Dialog.Close asChild>
                <button style={{
                  marginTop: '15px', padding: '8px 16px', backgroundColor: '#4285F4', 
                  color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer'
                }}>
                  Close
                </button>
              </Dialog.Close>
            </Dialog.Content>
          </Dialog.Portal>
        </Dialog.Root>
      )}
    </div>
  );
};

export default MenuContent;
