// Utility function to verify that the closest locations are properly highlighted
export const verifyClosestLocations = (sortedLocations) => {
  if (!sortedLocations || !Array.isArray(sortedLocations)) {
    console.error('Invalid locations array');
    return false;
  }

  // Check if exactly 5 locations are marked as close
  const closeLocations = sortedLocations.filter(loc => loc.isClose);
  if (closeLocations.length !== 5) {
    console.error(`Expected 5 closest locations, found ${closeLocations.length}`);
    return false;
  }

  // Verify that the closest 5 locations are actually the ones marked
  const firstFiveDistances = sortedLocations.slice(0, 5).map(loc => loc.distance);
  const markedDistances = closeLocations.map(loc => loc.distance);

  const areEqual = JSON.stringify(firstFiveDistances.sort()) === JSON.stringify(markedDistances.sort());
  if (!areEqual) {
    console.error('Marked locations do not match the actual closest locations');
    return false;
  }

  // Verify that distances are properly sorted
  const isSorted = sortedLocations.every((loc, i) =>
    i === 0 || loc.distance >= sortedLocations[i-1].distance
  );
  if (!isSorted) {
    console.error('Locations are not properly sorted by distance');
    return false;
  }

  return true;
};
