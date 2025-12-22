import { addVoucherHandler, manageVoucherHandler, filterVoucherHandler } from "../main/ui.js";
import { logoutHandler } from "../auth/auth-ui.js";



export function addEventListeners() {

    const voucherSearchForm = document.querySelector("#vouchers-search-form");
    voucherSearchForm.addEventListener("change", async (evt) => {
        await filterVoucherHandler(evt);
    });

    const addVoucherSubmit = document.querySelector(".add-voucher-submit");
    addVoucherSubmit.addEventListener("click", async () => {
        await addVoucherHandler();
    });

    const vouchersData = document.querySelector("#vouchers-data");
    vouchersData.addEventListener("click", async (evt) => {
        await manageVoucherHandler(evt);

    });

    const logout = document.querySelector(".logout");
    logout.addEventListener("click", async () => {
        await logoutHandler();
    });
}

