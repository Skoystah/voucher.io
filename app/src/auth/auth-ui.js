import { login, logout } from "../api/auth.js";

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
        localStorage.setItem("isAdmin", data.is_admin);
        window.location.href = "index.html"
    } catch (error) {
        window.alert("Login failed");
    } finally {
        form.reset();
    }
};

export async function logoutHandler() {
    localStorage.removeItem("isAdmin");
    try {
        await logout();
    } catch (error) {
        window.alert("Logout failed");
    }
    finally {
        window.location.reload();
    }
}
