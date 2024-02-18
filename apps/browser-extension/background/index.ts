import { sendMessageToContentScript, type MessageToBackgroundRequest } from 'lib/utils/messaging';
import browser from 'webextension-polyfill';
import { suggest } from '~lib/llm';

// browser.runtime.onInstalled.addListener((details) => {
// 	if (details.reason === 'install') {
// 		browser.runtime.openOptionsPage();
// 	}
// });

// browser.commands.onCommand.addListener(async (command) => {
// 	if (command === 'toggle-recording') {
// 		sendMessageToContentScript({ command: 'toggle-recording' });
// 	}
// });

browser.runtime.onMessage.addListener(async (message: MessageToBackgroundRequest) => {
	switch (message.action) {
		case 'suggest': {
			// send response back
			const aiRes = await suggest(message.content);
			return aiRes;
		}
		case 'openOptionsPage':
			browser.runtime.openOptionsPage();
			break;
	}
});

export {};
