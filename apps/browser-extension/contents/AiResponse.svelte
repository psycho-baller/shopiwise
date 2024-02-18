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
	import { aiResponse, updateAiResponse, type AiProductIntention } from '~lib/stores/aiResponse';
	import browser from 'webextension-polyfill';
	import Hoverable from '~components/Hoverable.svelte';
	// import { options } from '~lib/stores/options';
	let productAiResponse: AiProductIntention[];
	onMount(async () => {
		// Get the product ID (ASIN) from the URL
		const url = window.location.href;
		const productId = url.split('/dp/')[1].split('/')[0].split('?')[0];

		// check if the product is already in local storage
		await aiResponse.init();
		console.log($aiResponse);
		productAiResponse = $aiResponse[productId];
		console.log(productAiResponse);
		if (!productAiResponse) {
			console.log('fetching', $aiResponse, productId);
			// if not, send a message to the background script to fetch the product
			const response = (await browser.runtime.sendMessage({
				action: 'fetchIntentions',
				productTitle: document.title?.split(':')[0],
				userInfo: '$options'
			})) as AiProductIntention[];
			console.log(response);
			updateAiResponse(productId, response);
			productAiResponse = response;
		}
	});
</script>

{#if productAiResponse}
	<div id="" class="bg-teal-500">
		{#each productAiResponse as product}
			<Hoverable character={product} />
		{/each}
	</div>
{:else}
	<div class="bg-red-500">
		<p>Loading...</p>
	</div>
{/if}
