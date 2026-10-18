import { API_URL } from "../config/config.js";

function toErrorMessage(response, fallback) {
    return response.text()
        .then((text) => {
            try {
                const payload = JSON.parse(text);
                return payload?.detail || payload?.message || text || fallback;
            } catch {
                return text || fallback;
            }
        })
        .catch(() => fallback);
}

export async function getVouchers(input) {
    const params = new URLSearchParams();

    const duration = input.get("duration");
    if (duration && duration.toLowerCase() !== "any") {
        params.set("duration", duration);
    }

    const includeUsed = input.get("include-used") === "true" || input.get("include-used") === true;
    params.set("includeUsed", String(includeUsed));

    const url = new URL(`${API_URL}/vouchers`);
    for (const [key, value] of params.entries()) {
        url.searchParams.set(key, value);
    }

    const response = await fetch(url, {
        method: "GET",
        credentials: "include",
    });

    if (!response.ok) {
        throw new Error(await toErrorMessage(response, `Request failed: ${response.status}`));
    }

    return await response.json();
}

export async function addVoucher(input) {
    const inputCode = String(input.get("input-code") ?? "").trim();
    const inputDuration = String(input.get("input-duration") ?? "").trim();

    if (!inputCode || !inputDuration) {
        throw new Error("Code and duration are required");
    }

    const response = await fetch(`${API_URL}/vouchers`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            code: inputCode,
            duration: inputDuration,
        }),
    });

    if (!response.ok) {
        throw new Error(await toErrorMessage(response, `Request failed: ${response.status}`));
    }

    return await response.json().catch(() => ({}));
}

export async function addVouchersFile(formData) {
    const response = await fetch(`${API_URL}/vouchers/upload-file`, {
        method: "POST",
        credentials: "include",
        body: formData,
    });

    if (!response.ok) {
        throw new Error(await toErrorMessage(response, `Request failed: ${response.status}`));
    }

    return await response.json().catch(() => ({}));
}

export async function useVoucher(code) {
    const safeCode = encodeURIComponent(String(code));
    const response = await fetch(`${API_URL}/vouchers/${safeCode}`, {
        method: "PUT",
        credentials: "include",
    });

    if (!response.ok) {
        throw new Error(await toErrorMessage(response, `Request failed: ${response.status}`));
    }
}

export async function deleteVoucher(code) {
    const safeCode = encodeURIComponent(String(code));
    const response = await fetch(`${API_URL}/vouchers/${safeCode}`, {
        method: "DELETE",
        credentials: "include",
    });

    if (!response.ok) {
        throw new Error(await toErrorMessage(response, `Request failed: ${response.status}`));
    }
}
