// Haversine formula to calculate distance between two points
const calculateDistance = (lat1, lon1, lat2, lon2) => {
  const R = 3959; // Earth's radius in miles
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a =
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  const distance = R * c;
  return Math.round(distance * 100) / 100; // Round to 2 decimal places
};

// Sort locations by distance from user location and mark the 5 closest
export const sortLocationsByDistance = (locations, userLocation) => {
  if (!locations || !userLocation) return [];

  return locations
      .map(location => ({
          ...location,
          distance: calculateDistance(
              userLocation.lat,
              userLocation.lng,
              location.lat,
              location.lng
          )
      }))
      .sort((a, b) => a.distance - b.distance)
      .map((location, index) => ({
          ...location,
          isClose: index < 5 // Mark the 5 closest locations
      }));
};