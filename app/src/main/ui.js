import { addVouchersFile, addVoucher, useVoucher, deleteVoucher, getVouchers } from "../api/vouchers.js";

export async function addVoucherHandler() {

    const form = document.querySelector("#vouchers-add-form");
    const formInput = new FormData(form);

    const inputCode = formInput.get("input-code");
    const inputFile = formInput.get("file");

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
        else if (window.confirm(`Are you sure you want to add voucher with code ${inputCode}?`)) {
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
export async function manageVoucherHandler(evt) {
    if (evt.target.dataset.action === 'use') {
        if (window.confirm(`Are you sure you want to use voucher ${evt.target.dataset.voucherCode}?`)) {
            await useVoucher(evt.target.dataset.voucherCode);
            fillVoucherScreen();
        };
    }
    if (evt.target.dataset.action === 'delete') {
        if (window.confirm(`Are you sure you want to permanently REMOVE voucher ${evt.target.dataset.voucherCode}?`)) {
            await deleteVoucher(evt.target.dataset.voucherCode);
            fillVoucherScreen();
        };
    }
}

export async function filterVoucherHandler(evt) {
    if (evt.target.className === "filter-voucher") {
        await fillVoucherScreen();
    }
}

export async function fillVoucherScreen() {

    const form = document.querySelector("#vouchers-search-form");
    const formInput = new FormData(form);

    try {
        presentVouchers(await getVouchers(formInput));
    } catch (error) {
        presentVouchers([]);
        throw error;
    }

    showAdminFunction();
}

function presentVouchers(data) {
    const vouchersData = document.querySelector("#vouchers-data");

    //remove existing content
    vouchersData.replaceChildren();

    if (data.length === 0) {
        const para = document.createElement("p");
        para.append("No vouchers found! :(");
        vouchersData.append(para);
        return;
    }

    //TODO - refactor table creation
    //add voucher table
    const voucherTable = document.createElement("table");
    voucherTable.id = "vouchers-table"
    vouchersData.appendChild(voucherTable);

    const voucherTableHead = document.createElement("thead");
    voucherTable.appendChild(voucherTableHead);

    const voucherTableRow = document.createElement("tr");
    voucherTableHead.appendChild(voucherTableRow);

    const codeHeader = document.createElement("th");
    codeHeader.textContent = "Code";
    voucherTableRow.appendChild(codeHeader);

    const durationHeader = document.createElement("th");
    durationHeader.textContent = "Duration";
    voucherTableRow.appendChild(durationHeader);

    const availableHeader = document.createElement("th");
    availableHeader.textContent = "Available";
    voucherTableRow.appendChild(availableHeader);

    const actionHeader = document.createElement("th");
    actionHeader.textContent = "Action";
    voucherTableRow.appendChild(actionHeader);

    const voucherTableBody = document.createElement("tbody");
    voucherTable.appendChild(voucherTableBody);

    data.forEach(item => {
        const voucherTableRow = document.createElement("tr");
        voucherTableBody.appendChild(voucherTableRow);

        const codeData = document.createElement("td");
        codeData.textContent = `${item.code}`;
        voucherTableRow.appendChild(codeData);
        const durationData = document.createElement("td");
        durationData.textContent = `${item.duration}`;
        voucherTableRow.appendChild(durationData);
        const availableData = document.createElement("td");
        availableData.textContent = translateUsedAvailable(item.used);
        voucherTableRow.appendChild(availableData);
        const actionData = document.createElement("td");


        if (!item.used) {
            const useButton = document.createElement("button");
            useButton.className = "use-button"
            useButton.textContent = "Use";
            useButton.dataset.voucherCode = item.code;
            useButton.dataset.action = "use";
            actionData.appendChild(useButton);
        } else {
            const deleteButton = document.createElement("button");
            deleteButton.className = "delete-button"
            deleteButton.textContent = "Remove";
            deleteButton.dataset.voucherCode = item.code;
            deleteButton.dataset.action = "delete";
            actionData.appendChild(deleteButton);
        }
        voucherTableRow.appendChild(actionData);
    });
}

function translateUsedAvailable(used) {
    return used ? "no" : "yes";
}

function showAdminFunction() {
    const isAdmin = localStorage.getItem("isAdmin")
    const addVouchersSection = document.querySelector("#vouchers-add")
    if (isAdmin === "true") {
        addVouchersSection.style.display = "block";
    } else {
        addVouchersSection.style.display = "none";
    }
}

export function showVoucherResultOk(message) {

    const addVoucherResult = document.querySelector("#add-voucher-result");

    addVoucherResult.style.color = "green";
    addVoucherResult.style.display = "block";
    addVoucherResult.textContent = message;
}

export function showVoucherResultError(message) {

    const addVoucherResult = document.querySelector("#add-voucher-result");

    addVoucherResult.style.color = "red";
    addVoucherResult.style.display = "block";
    addVoucherResult.textContent = message;
}
