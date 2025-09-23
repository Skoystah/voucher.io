import { getVouchers, useVoucher, deleteVoucher } from "../api/vouchers.js";

export async function fillVoucherScreen() {

    const form = document.querySelector("#vouchers-search-form");
    const formInput = new FormData(form);

    try {
        presentVouchers(await getVouchers(formInput));
    } catch (error) {
        console.log("failed to load vouchers :", error);
        presentVouchers([])
    }
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

    //add voucher table
    const voucherTable = document.createElement("table");
    voucherTable.id = "vouchers-table"
    vouchersData.appendChild(voucherTable);

    const voucherTableRow = document.createElement("tr");
    voucherTable.appendChild(voucherTableRow);

    const codeHeader = document.createElement("th");
    codeHeader.textContent = "Code";
    voucherTableRow.appendChild(codeHeader);

    const durationHeader = document.createElement("th");
    durationHeader.textContent = "Duration";
    voucherTableRow.appendChild(durationHeader);

    const availableHeader = document.createElement("th");
    availableHeader.textContent = "Available?";
    voucherTableRow.appendChild(availableHeader);


    data.forEach(item => {
        const voucherTableRow = document.createElement("tr");
        voucherTable.appendChild(voucherTableRow);

        const codeData = document.createElement("td");
        codeData.textContent = `${item.code}`;
        voucherTableRow.appendChild(codeData);
        const durationData = document.createElement("td");
        durationData.textContent = `${item.duration}`;
        voucherTableRow.appendChild(durationData);
        const availableData = document.createElement("td");
        availableData.textContent = translateUsedAvailable(item.used);
        voucherTableRow.appendChild(availableData);

        if (!item.used) {
            const useButton = document.createElement("button");
            useButton.className = "use-button"
            useButton.textContent = "Use voucher";
            useButton.dataset.voucherCode = item.code;
            useButton.dataset.action = "use";
            voucherTableRow.appendChild(useButton);
        } else {
            const deleteButton = document.createElement("button");
            deleteButton.className = "delete-button"
            deleteButton.textContent = "Remove voucher";
            deleteButton.dataset.voucherCode = item.code;
            deleteButton.dataset.action = "delete";
            voucherTableRow.appendChild(deleteButton);
        }
    });
}

function translateUsedAvailable(used) {
    return used ? "no" : "yes";
}
