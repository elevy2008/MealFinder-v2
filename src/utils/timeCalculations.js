export const calculateDepartureTime = (locationTime, walkingDuration) => {
    const now = new Date();

    // Split locationTime and ensure proper parsing
    const timeParts = locationTime.split(':');
    if (timeParts.length !== 2) {
        return "Invalid time format";
    }

    const hours = parseInt(timeParts[0], 10);
    const minutes = parseInt(timeParts[1], 10);

    // Validate parsed hours and minutes
    if (isNaN(hours) || isNaN(minutes)) {
        return "Invalid time values";
    }

    // Create arrival time
    const arrivalTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hours, minutes);

    // Ensure walkingDuration is a valid number
    const walkingMinutes = parseInt(walkingDuration, 10)+8;
    if (isNaN(walkingMinutes)) {
        return "Invalid walking duration";
    }

    // Calculate time until arrival (in minutes)
    const timeUntilArrival = Math.floor((arrivalTime - now) / 60000);

    // Calculate time until leave (in minutes) with a 5-minute cushion
    const timeUntilLeave = timeUntilArrival - walkingMinutes - 9;

    // Calculate departure time (as a Date object)
    const departureTime = new Date(now.getTime() + timeUntilLeave * 60000);

    // Format departure time as a readable string (e.g., "HH:mm")
    const formattedDepartureTime = departureTime.toTimeString().split(' ')[0].slice(0, 5); // Extract "HH:mm"

    // Return both when to leave and the time until leave in one line
    return `Leave/Start Walking At ${formattedDepartureTime} pm`;
};
