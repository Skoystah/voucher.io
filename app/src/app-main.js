import { fillVoucherScreen } from "./main/ui.js";
import { addEventListeners } from "./main/dom.js";

// ON LOADING
try {
    await fillVoucherScreen();
    addEventListeners();
} catch (error) {
    // TODO add catch on forbidden ?
    window.location.href = "auth.html";
}


