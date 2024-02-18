import { sendMessageToBackground } from '~lib/utils/messaging';
import { createStoreSyncedWithStorage } from './createStore';

export const content = createStoreSyncedWithStorage<string>({
	key: 'content',
	initialValue: ''
});

let timeoutId: NodeJS.Timeout;
content.subscribe((value) => {
	// only send if length > 100
	if (value.length < 100) return;
	console.log(value);
	// debounce: wait 2 second before sending
	clearTimeout(timeoutId);
	timeoutId = setTimeout(() => {
		sendMessageToBackground({ action: 'updateContent', content: value });
	}, 2000);
});
