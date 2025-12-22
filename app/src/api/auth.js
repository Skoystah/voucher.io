import { API_URL } from "../config/config.js";

export async function login(input) {

    const inputUserName = input.get("username");
    const inputPassword = input.get("password");

    const url = API_URL.concat("/login");
    const request = new Request(
        url,
        {
            method: "POST",
            headers: { 'Content-Type': 'application/json', },
            credentials: "include",
            body: JSON.stringify({
                name: inputUserName,
                password: inputPassword,
            }),
        }
    );

    const response = await fetch(request);
    if (!response.ok) {
        throw new Error(`Login failed: ${response.status}`);
    }
    return await response.json();
}

export async function logout() {

    const url = API_URL.concat("/logout");
    const request = new Request(
        url,
        {
            method: "POST",
            credentials: "include",
        }
    );

    const response = await fetch(request);
    if (!response.ok) {
        throw new Error(`Logout failed: ${response.status}`);
    }
}
