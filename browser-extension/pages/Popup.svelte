<script lang="ts">
	import { onMount } from 'svelte';
	import { options } from '~lib/stores/options';

	onMount(async () => {
		await options.init();
	});
</script>

<div class="flex flex-col gap-y-2 p-8">
	<h3 id="contact-info-heading" class="text-2xl font-extrabold text-gray-900">
		Personalize your responses
	</h3>

	<div class="mt-6">
		<label for="user-info" class="text-md block font-medium text-gray-700">Who are you</label>
		<p class="text-md mt-1 text-gray-500">
			Talk about yourself, your interests, and your spending habits. This will help us generate more
			accurate responses to the products you're interested in.
		</p>
		<div class="mt-1">
			<textarea
				rows="4"
				id="user-info"
				name="user-info"
				class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
				bind:value={$options.userInfo}
			/>
		</div>
	</div>
</div>
