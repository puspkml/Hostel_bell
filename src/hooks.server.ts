import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
	// You can add any global logic here if needed
	return resolve(event);
};
