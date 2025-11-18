import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';

/**
 * Loads bell logs from Flask backend.
 */
export const load: PageServerLoad = async ({ url }) => {
	try {
		// Extract sorting options from query params (optional)
		const sortKey = url.searchParams.get('sort') || 'id';
		const sortOrder = url.searchParams.get('order') === 'asc' ? 'asc' : 'desc';

		// Fetch data from Flask backend
		const res = await fetch(`http://127.0.0.1:5000/bell_log?sort=${sortKey}&order=${sortOrder}`);

		if (!res.ok) {
			throw error(500, `Failed to fetch bell logs: ${res.statusText}`);
		}

		const logs = await res.json();

		// Ensure each log has expected fields
		const formattedLogs = logs.map((log: any) => ({
			id: log.id,
			name: log.name,
			bell_type: log.bell_type,
			date_logged: log.date_logged,
			ring_time: log.ring_time
		}));

		return {
			logs: formattedLogs,
			sortKey,
			sortOrder
		};
	} catch (err) {
		console.error('Error fetching bell logs:', err);
		throw error(500, 'Unable to load bell logs from Flask.');
	}
};
