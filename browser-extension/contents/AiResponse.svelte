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
	import { Motion, animate } from 'svelte-motion';
	import { options } from '~lib/stores/options';
	let productAiResponse: AiProductIntention[];
	const variants = {
		visible: (i) => ({
			opacity: 1,
			transition: {
				delay: i * 0.3
			}
		}),
		hidden: { opacity: 0 }
	};
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
				userInfo: $options.userInfo
			})) as AiProductIntention[];
			console.log(response);
			updateAiResponse(productId, response);
			productAiResponse = response;
		}
	});
</script>

{#if productAiResponse}
	<div class="mb-3 flex flex-col gap-y-4 border-b-2 border-gray-300 pb-3">
		<h3 class="text-center text-2xl font-bold">Unconscious motivations</h3>
		<Motion let:motion {variants} animate="visible" initial="hidden">
			<div use:motion id="intentions" class="flex flex-col gap-y-4 font-bold will-change-transform">
				{#each productAiResponse as product, i}
					<Hoverable
						custom={0.25 + i}
						initial="hidden"
						{variants}
						character={product}
						animate="visible"
					/>
				{/each}
			</div>
		</Motion>
	</div>
	<!-- {:else}
	<div class="bg-red-500">
		<p>Loading...</p>
	</div> -->
{/if}
