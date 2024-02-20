import { writable } from 'svelte/store';
import { Storage } from '@plasmohq/storage';

export function createStoreSyncedWithStorage<T>({
	key,
	initialValue
}: {
	key: string;
	initialValue: T;
}) {
	const { subscribe, set, update } = writable<T>(initialValue);
	const storage = new Storage({
		copiedKeyList: ['shield-modulation'],
		area: 'local'
	});

	async function init() {
		const valueFromStorage = await storage.get<T>(key);
		set(valueFromStorage || initialValue);
	}

	async function setValue(value: T) {
		await storage.set(key, value);
		set(value);
	}

	return {
		subscribe,
		init,
		set: setValue,
		update
	};
}
