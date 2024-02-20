import { createStoreSyncedWithStorage } from './createStore';
import { get } from 'svelte/store';

export type AiProductIntention = {
	title: string;
	description: string;
};
export const aiResponse = createStoreSyncedWithStorage<{
	[key: string]: AiProductIntention[];
}>({
	key: 'aiResponse',
	initialValue: {}
});

export function updateAiResponse(key: string, value: AiProductIntention[]) {
	aiResponse.set({ ...get(aiResponse), [key]: value });
}
