export async function suggest(text: string): Promise<string> {
	return 'This is a suggestion';
	const res = await fetch('http://fastapi.localhost/chat/123', {
		method: 'POST',
		body: JSON.stringify({ user_id: '123', message: text }),
		headers: {
			'Content-Type': 'application/json'
		}
	});
	const json = await res.json();
	console.log(json);
	return json.message;
}
