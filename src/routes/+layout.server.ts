import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async () => {
  // No authentication, just return empty object
  return {};
};
