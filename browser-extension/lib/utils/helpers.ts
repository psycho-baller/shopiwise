import { sendMessageToBackground } from './messaging';

export function openOptionsPage() {
	sendMessageToBackground({ action: 'openOptionsPage' });
}
