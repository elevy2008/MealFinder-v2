// Verification script for walking duration calculations
const testDistances = [
  { distance: 1, expectedMinutes: 19 },    // 1 mile should take ~19 minutes at 3.1 mph
  { distance: 2, expectedMinutes: 39 },    // 2 miles should take ~39 minutes
  { distance: 0.5, expectedMinutes: 10 },  // 0.5 miles should take ~10 minutes
  { distance: 3.1, expectedMinutes: 60 }   // 3.1 miles should take exactly 60 minutes
];

const calculateDuration = (distance) => {
  // Same calculation as in LocationList.jsx
  const hours = distance / 3.1;
  const minutes = Math.round(hours * 60);
  return minutes;
};

console.log('Verifying duration calculations...\n');

let allTestsPassed = true;
testDistances.forEach(test => {
  const calculatedMinutes = calculateDuration(test.distance);
  const passed = calculatedMinutes === test.expectedMinutes;
  console.log(`Test for ${test.distance} miles:`);
  console.log(`Expected: ${test.expectedMinutes} minutes`);
  console.log(`Calculated: ${calculatedMinutes} minutes`);
  console.log(`Status: ${passed ? 'PASSED' : 'FAILED'}\n`);
  if (!passed) allTestsPassed = false;
});

console.log(`Overall verification status: ${allTestsPassed ? 'PASSED' : 'FAILED'}`);
