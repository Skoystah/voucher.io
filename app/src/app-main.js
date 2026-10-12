import { fillVoucherScreen } from "./main/ui.js";
import { addEventListeners } from "./main/dom.js";

// ON LOADING
try {
    await fillVoucherScreen();
    console.log("done voucherscreen");
    addEventListeners();
} catch (error) {
    console.error(error);
    // TODO add catch on forbidden ?
    window.location.href = "auth.html";
}


