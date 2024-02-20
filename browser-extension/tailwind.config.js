/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./**/*.{html,svelte,ts}', '../../packages/**/*.{html,svelte,ts}'],
	theme: {
		extend: {}
	},
	plugins: [require('@tailwindcss/forms')]
};
