import { fillVoucherScreen } from "./ui/ui.js";
import { addEventListeners, getAuthToken } from "./dom/dom.js";

// ON LOADING
const token = getAuthToken();
if (!token) {
    console.log("No token!");
    window.location.href = "auth.html";
}
await fillVoucherScreen();
addEventListeners();

