import { loginHandler } from "./auth-ui.js";

export function addAuthEventListeners() {
    const loginSubmit = document.querySelector(".login-submit");
    loginSubmit.addEventListener("click", async (evt) => {
        await loginHandler(evt);
    });
}
