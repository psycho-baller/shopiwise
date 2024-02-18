<script lang="ts">
	import { fade } from 'svelte/transition';
	import { scale } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	export let character: { title: string; description: string };

	let hovering = false;
	let requested = false;
	let resolve = null;

	const enter = () => {
		hovering = true;
	};

	const leave = () => (hovering = false);
</script>

<div class="relative" on:mouseenter={enter} on:mouseleave={leave} role="tooltip">
	{character.title}

	{#if hovering}
		<div
			in:scale={{ duration: 150, easing: quintOut, opacity: 0 }}
			class="absolute left-8 top-4 z-50 w-48 rounded-lg border bg-white p-2 shadow-xl"
		>
			<h3 class="text-lg font-semibold">
				{character.title}
			</h3>

			<div in:fade={{ duration: 150 }}>
				{character.description}
			</div>
		</div>
	{/if}
</div>
