<script lang="ts" context="module">
	import { onMount } from 'svelte';
	import type { PlasmoCSConfig, PlasmoGetInlineAnchor } from 'plasmo';

	import cssText from 'data-text:~style.css';
	export const getStyle = () => {
		const style = document.createElement('style');
		style.textContent = cssText;
		return style;
	};

	export const config: PlasmoCSConfig = {
		matches: ['https://www.amazon.com/*', 'https://www.amazon.ca/*'],
		run_at: 'document_idle'
	};
	export const getInlineAnchor: PlasmoGetInlineAnchor = async () =>
		document.getElementById('quantityRelocate_feature_div');
</script>

<script lang="ts">
	import { aiResponse, updateAiResponse } from '~lib/stores/aiResponse';
	import browser from 'webextension-polyfill';
	let productDescription: string;
	onMount(async () => {
		// Get the product ID (ASIN) from the URL
		const url = window.location.href;
		const productId = url.split('/dp/')[1].split('/')[0];

		// check if the product is already in local storage
		aiResponse.init();
		console.log($aiResponse);
		$: productDescription = $aiResponse[productId];
		if (!productDescription) {
			// if not, send a message to the background script to fetch the product
			const response = await browser.runtime.sendMessage({
				action: 'suggest',
				productId
			});
			updateAiResponse(productId, response);
		}
	});
</script>

{#if productDescription}
	<div id="" class="">
		{productDescription}
	</div>
{/if}
