// Verification utility for accordion functionality
export const verifyAccordionState = () => {
  const accordion = document.querySelector('[data-testid="accordion-container"]');
  if (!accordion) {
    console.error('Accordion container not found');
    return false;
  }

  // Check initial visibility
  const isVisible = window.getComputedStyle(accordion).display !== 'none';
  console.log('Initial accordion visibility:', isVisible);

  // Check content height and transitions
  const content = accordion.querySelector('[role="region"]');
  const contentHeight = content?.scrollHeight || 0;
  const styles = window.getComputedStyle(content || accordion);

  // Verify transition properties
  const hasTransitions = styles.transition.includes('transform') &&
                        styles.transition.includes('opacity');

  // Verify z-index layering
  const header = accordion.querySelector('[role="button"]');
  const headerZIndex = window.getComputedStyle(header).zIndex;
  const contentZIndex = styles.zIndex;

  const verificationResults = {
    isVisible,
    contentHeight,
    hasTransitions,
    zIndexLayering: {
      header: headerZIndex,
      content: contentZIndex,
    },
    timestamp: new Date().toISOString(),
    userAgent: navigator.userAgent
  };

  console.log('Accordion verification results:', verificationResults);
  return verificationResults;
};

// Add verification to window for console access
window.verifyAccordion = verifyAccordionState;

// Add toggle verification
window.toggleAndVerify = async () => {
  const button = document.querySelector('[role="button"]');
  if (button) {
    button.click();
    // Wait for transition
    await new Promise(resolve => setTimeout(resolve, 300));
    return verifyAccordionState();
  }
  return null;
};
