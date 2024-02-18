export async function fetchIntentions(product_title: string, user_info: string) {
	const res = await fetch('http://fastapi.localhost/intentions', {
		method: 'POST',
		body: JSON.stringify({ product_title, user_info }),
		headers: {
			'Content-Type': 'application/json'
		}
	});
	const json = await res.json();
	console.log(json);
	return json.intentions;
}
