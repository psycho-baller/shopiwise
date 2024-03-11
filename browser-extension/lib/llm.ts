import { BASE_API_URL } from "./utils/constants";

export async function fetchIntentions(productTitle: string, userInfo: string) {
	const res = await fetch(`${BASE_API_URL}/intentions`, {
		method: 'POST',
		body: JSON.stringify({ productTitle, userInfo }),
		headers: {
			'Content-Type': 'application/json'
		}
	});
	const json = await res.json();
	console.log(json);
	return json.intentions;
}
