import { type MessageToBackgroundRequest } from 'lib/utils/messaging';
import browser from 'webextension-polyfill';
import { fetchIntentions } from '~lib/llm';

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
		case 'fetchIntentions': {
			// send response back
			console.log('suggesting');
			const aiRes = await fetchIntentions(message.productTitle, message.userInfo);
			return aiRes;
		}
		case 'openOptionsPage':
			browser.runtime.openOptionsPage();
			break;
	}
});

export {};
