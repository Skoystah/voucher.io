import { API_URL } from "../config.js";

export async function loginHandler(e) {
    e.preventDefault();

    const form = document.querySelector("#user-login-form");
    const formInput = new FormData(form);

    const inputUserName = formInput.get("username");
    const inputPassword = formInput.get("password");

    if (!inputUserName) {
        window.alert("User name required");
        return
    }
    if (!inputPassword) {
        window.alert("Password required");
        return
    }

    try {
        const data = await login(formInput);
        console.log(data);
        localStorage.setItem("token", data.token);
        localStorage.setItem("isAdmin", data.is_admin);
        console.log("Redirecting to index")
        window.location.href = "index.html"
    } catch (error) {
        console.error(error);
        window.alert("Login failed");
    }
};

async function login(input) {

    const inputUserName = input.get("username");
    const inputPassword = input.get("password");

    const url = API_URL.concat("/login");
    const request = new Request(
        url,
        {
            method: "POST",
            headers: { 'Content-Type': 'application/json', },
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


// const loginSubmit = document.querySelector("#login-submit");
const loginSubmit = document.querySelector(".login-submit");
//
loginSubmit.addEventListener("click", async (e) => {
    await loginHandler(e);
});
