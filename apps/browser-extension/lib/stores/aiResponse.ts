import { createStoreSyncedWithStorage } from './createStore';

export const aiResponse = createStoreSyncedWithStorage<{ [key: string]: string }>({
	key: 'aiResponse',
	initialValue: {
		hi: 'hello'
	}
});

export function updateAiResponse(key: string, value: string) {
	aiResponse.update((responses) => ({ ...responses, [key]: value }));
}
