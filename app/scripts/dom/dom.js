import { addVoucher, addVouchersFile, useVoucher, deleteVoucher } from "../api/vouchers.js";
import { fillVoucherScreen } from "../ui/ui.js";

export async function addVoucherHandler() {

    const form = document.querySelector("#vouchers-add-form");
    const formInput = new FormData(form);

    const inputCode = formInput.get("input-code");
    const inputFile = formInput.get("input-file");

    if (inputFile.name) {
        if (inputCode) {
            showVoucherResultError('Either add a file or add a code and duration');
        }
        else if (window.confirm("Are you sure you want to add vouchers from this file?")) {
            try {
                await addVouchersFile(formInput);
                await fillVoucherScreen();
                // TODO : feedback on which vouchers were added and which were not
                showVoucherResultOk('Successfully added vouchers')
                form.reset();
            } catch (error) {
                showVoucherResultError(error.message);
            }
        };
    } else {
        if (!inputCode) {
            showVoucherResultError('Both code and duration need to be provided');
        }
        else if (window.confirm("Are you sure you want to add this voucher?")) {
            try {
                await addVoucher(formInput);
                await fillVoucherScreen();
                showVoucherResultOk('Successfully added voucher')
                form.reset();
            } catch (error) {
                showVoucherResultError(error.message);
            }
        };
    }
}

function showVoucherResultOk(message) {

    const addVoucherResult = document.querySelector("#add-voucher-result");

    addVoucherResult.style.color = "green";
    addVoucherResult.style.display = "block";
    addVoucherResult.textContent = message;
}

function showVoucherResultError(message) {

    const addVoucherResult = document.querySelector("#add-voucher-result");

    addVoucherResult.style.color = "red";
    addVoucherResult.style.display = "block";
    addVoucherResult.textContent = message;
}

export function addEventListeners() {

    const voucherSearchForm = document.querySelector("#vouchers-search-form");
    voucherSearchForm.addEventListener("change", async (evt) => {
        if (evt.target.className === "filter-voucher") {
            await fillVoucherScreen();
        }
    });

    const addVoucherSubmit = document.querySelector(".add-voucher-submit");
    addVoucherSubmit.addEventListener("click", async () => {
        await addVoucherHandler();
    });

    const vouchersData = document.querySelector("#vouchers-data");
    vouchersData.addEventListener("click", async (evt) => {
        console.log("processing event for ", evt);
        if (evt.target.dataset.action === 'use') {
            if (window.confirm("Are you sure you want to use this voucher?")) {
                await useVoucher(evt.target.dataset.voucherCode);
                // TODO - acceptable to fetch all again?
                fillVoucherScreen();
            };
        }
        if (evt.target.dataset.action === 'delete') {
            if (window.confirm("Are you sure you want to permanently REMOVE this voucher?")) {
                await deleteVoucher(evt.target.dataset.voucherCode);
                // TODO - acceptable to fetch all again?
                fillVoucherScreen();
            };
        }
    });

    const logout = document.querySelector(".logout");
    logout.addEventListener("click", logoutHandler);
}

export function getAuthToken() {
    return localStorage.getItem("token");
}

function logoutHandler() {
    localStorage.removeItem("token");
    localStorage.removeItem("isAdmin");
    window.location.reload();
}

