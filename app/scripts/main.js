async function getData() {
    const url = "http://localhost:8000/vouchers";
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        const json = await response.json()bmit.addEventListener("click", getData)
