export async function fetchIntentions(productTitle: string, userInfo: string) {
	const res = await fetch('http://fastapi.localhost/intentions', {
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
