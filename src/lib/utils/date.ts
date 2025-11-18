export function formatScheduleDate(dateStr: string, timeStr: string) {
	// Combine into ISO-like format
	const dateTime = new Date(`${dateStr}T${convertTo24Hour(timeStr)}`);

	if (isNaN(dateTime.getTime())) {
		return { date: "Invalid Date", time: "Invalid Time" };
	}

	const formattedDate = dateTime.toLocaleDateString("en-IN", {
		weekday: "short",
		day: "2-digit",
		month: "short",
		year: "numeric"
	});

	const formattedTime = dateTime.toLocaleTimeString("en-IN", {
		hour: "numeric",
		minute: "2-digit",
		hour12: true
	});

	return { date: formattedDate, time: formattedTime };
}

function convertTo24Hour(timeStr: string) {
	// input: "05:00 AM", "08:00 PM"
	const [time, modifier] = timeStr.split(" ");
	let [hours, minutes] = time.split(":").map(Number);

	if (modifier.toLowerCase() === "pm" && hours < 12) hours += 12;
	if (modifier.toLowerCase() === "am" && hours === 12) hours = 0;

	return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:00`;
}
