<script lang="ts">
	import { fade } from 'svelte/transition';
	import { scale } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { Motion } from 'svelte-motion';

	export let character: { title: string; description: string },
		variants,
		initial = undefined,
		custom = undefined,
		animate = undefined;

	let hovering = false;
	let requested = false;
	let resolve = null;

	const enter = () => {
		hovering = true;
	};

	const leave = () => (hovering = false);
</script>

<Motion let:motion {variants} {initial} {animate} {custom}>
	<div use:motion on:mouseenter={enter} on:mouseleave={leave} class="relative" role="tooltip">
		{character.title}

		{#if hovering}
			<div
				in:scale={{ duration: 150, easing: quintOut, opacity: 0 }}
				class="absolute z-50 flex w-full flex-col gap-y-2 rounded-lg border bg-white p-2 shadow-xl"
			>
				<!-- <h3 class="text-lg font-semibold">
				{character.title}
			</h3> -->

				<div in:fade={{ duration: 150 }} class="font-medium text-gray-700">
					{character.description}
				</div>
			</div>
		{/if}
	</div>
</Motion>
