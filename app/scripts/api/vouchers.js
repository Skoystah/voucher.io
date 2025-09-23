import { API_URL } from "../config.js";

export async function getVouchers(input) {
    let params = new URLSearchParams();

    const duration = input.get("duration");
    if (duration && duration.toLowerCase() !== "any") {
        params.set("duration", duration)
    }

    const includeUsed = input.get("include-used");
    if (includeUsed) {
        params.set("includeUsed", includeUsed);
    } else {
        params.set("includeUsed", "false")
    }

    const query = params.toString();
    let url = API_URL.concat("/vouchers")
    if (query) {
        url = url.concat("?", query);
    }

    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
    }
    const data = await response.json();
    return data;
}

export async function addVoucher(input) {
    const inputCode = input.get("input-code");
    const inputDuration = input.get("input-duration");

    const url = API_URL.concat("/vouchers");
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


    const response = await fetch(request);
    // if (!response.ok) {
    //     const content = await response.json();
    //     throw new Error(content.detail);
    // }
}

export async function addVouchersFile(input) {

    const url = API_URL.concat("/vouchers/upload-file");
    const request = new Request(
        url,
        {
            method: "POST",
            body: input,
        }
    );

    const response = await fetch(request);
    if (!response.ok) {
        const content = await response.json();
        throw new Error(content.detail);
    }
}

export async function useVoucher(code) {
    const url = API_URL.concat("/vouchers/", code)
    const request = new Request(
        url,
        {
            method: "PUT",
        }
    );

    const response = await fetch(request);
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
    }
}

export async function deleteVoucher(code) {
    const url = API_URL.concat("/vouchers/", code)
    const request = new Request(
        url,
        {
            method: "DELETE",
        }
    );

    const response = await fetch(request);
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
    }
}
