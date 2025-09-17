import { API_URL } from "../config.js";

export async function getVouchers() {
    const form = document.getElementById("vouchers-search-form");
    const formInput = new FormData(form);

    let params = new URLSearchParams();

    params.set("includeUsed", "false");
    for (const [key, value] of formInput) {
        switch (key) {
            case "duration":
                if (value.toLowerCase() === "any") {
                    break
                };
                params.set("duration", value);
                break;
            case "include-used":
                params.set("includeUsed", value);
                break;
        }
    }

    const query = params.toString();
    let url = API_URL.concat("/vouchers")
    if (query) {
        url = url.concat("?", query);
    }

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error.message);
    }
}

export async function addVoucher(input) {
    const inputCode = input.get("inputCode");
    const inputDuration = input.get("inputDuration");

    const url = base_url.concat("/vouchers");
    const request = new Request(
        url,
        {
            method: "POST",
            headers: { 'Content-Type': 'application/json', },
            body: JSON.stringify({
                code: inputCode,
                duration: inputDuration,
            }),
        }
    );

    try {
        const response = await fetch(request);
        if (!response.ok) {
            // if (response.status === 409) {
            const content = await response.json();
            throw new Error(content.detail);
            // throw new Error(`Response status: ${response.status}`);
            // };
        }
    } catch (error) {
        throw error;
    }
}

export async function addVouchersFile(input) {

    const url = base_url.concat("/vouchers/upload-file");
    const request = new Request(
        url,
        {
            method: "POST",
            body: input,
        }
    );

    try {
        const response = await fetch(request);
        if (!response.ok) {
            // if (response.status === 409) {
            const content = await response.json();
            throw new Error(content.detail);
            // throw new Error(`Response status: ${response.status}`);
            // };
        }
    } catch (error) {
        throw error;
    }
}

export async function useVoucher(code) {
    const url = base_url.concat("/vouchers/", code)
    const request = new Request(
        url,
        {
            method: "PUT",
        }
    );

    try {
        const response = await fetch(request);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }
    } catch (error) {
        console.error(error.message);
    }
}

export async function deleteVoucher(code) {
    const url = base_url.concat("/vouchers/", code)
    const request = new Request(
        url,
        {
            method: "DELETE",
        }
    );

    try {
        const response = await fetch(request);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }
    } catch (error) {
        console.error(error.message);
    }
}
