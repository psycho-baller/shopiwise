import sharedConfig from 'tailwind-config/tailwind.config.js';

module.exports = {
	presets: [sharedConfig],
	plugins: [require('@tailwindcss/forms')]
};
