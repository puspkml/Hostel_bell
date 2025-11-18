import type { PageServerLoad, Actions } from './$types';
import { error, json } from '@sveltejs/kit';

// Fetch schedules from Flask
export const load: PageServerLoad = async ({ url }) => {
	try {
		const sortKey = url.searchParams.get('sort') || 'schedule_date';
		const sortOrder = url.searchParams.get('order') === 'desc' ? 'desc' : 'asc';

		// Call Flask API
		const res = await fetch(`http://127.0.0.1:5000/schedules?sort=${sortKey}&order=${sortOrder}`);
		if (!res.ok) throw error(500, 'Failed to fetch schedules from Flask');

		const schedules = await res.json();
		console.log('Fetched schedules:', schedules);

		return { schedules, sortKey, sortOrder };
	} catch (e) {
		console.error('Error fetching schedules:', e);
		throw error(500, 'Failed to fetch schedules.');
	}
};

export const actions: Actions = {
	deleteSchedule: async ({ request, url }) => {
		const formData = await request.formData();
		const scheduleId = Number(formData.get('scheduleId'));

		if (isNaN(scheduleId)) throw error(400, 'Invalid schedule ID');

		try {
			// Call Flask delete API
			const res = await fetch(`http://127.0.0.1:5000/delete/${scheduleId}`, {
				method: 'DELETE'
			});

			if (!res.ok) throw error(500, 'Flask delete failed');
			const result = await res.json();

			// Re-fetch schedules after delete
			const sortKey = url.searchParams.get('sort') || 'schedule_date';
			const sortOrder = url.searchParams.get('order') === 'desc' ? 'desc' : 'asc';

			const updatedRes = await fetch(`http://127.0.0.1:5000/schedules?sort=${sortKey}&order=${sortOrder}`);
			if (!updatedRes.ok) throw error(500, 'Failed to fetch updated schedules');
			const updatedSchedules = await updatedRes.json();

			return json({ success: true, message: result.message, schedules: updatedSchedules });
		} catch (e) {
			console.error('Error deleting schedule:', e);
			throw error(500, 'Failed to delete schedule.');
		}
	}
};
