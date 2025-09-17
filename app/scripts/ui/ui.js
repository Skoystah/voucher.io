import { getVouchers, useVoucher, deleteVoucher } from "../api/vouchers.js";

export async function fillVoucherScreen() {
    try {
        presentVouchers(await getVouchers());
    } catch (error) {
        console.log("failed to load vouchers :", error);
        presentVouchers([])
    }
}
function presentVouchers(data) {
    const vouchersData = document.getElementById("vouchers-data");

    //remove all existing vouchers
    while (vouchersData.firstChild) {
        vouchersData.removeChild(vouchersData.firstChild);
    }

    if (data.length === 0) {
        const para = document.createElement("p");
        para.textContent = "No vouchers found! :(";
        vouchersData.appendChild(para);
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


    for (const item of data) {
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
            useButton.className = "useButton"
            useButton.textContent = "Use voucher";
            voucherTableRow.appendChild(useButton);
        } else {
            const deleteButton = document.createElement("button");
            deleteButton.className = "deleteButton"
            deleteButton.textContent = "Remove voucher";
            voucherTableRow.appendChild(deleteButton);
        }
    }
    vouchersData.addEventListener("click", async (evt) => {
        if (evt.target.className == "useButton") {
            if (window.confirm("Are you sure you want to use this voucher?")) {
                await useVoucher(item.code);
                // TODO - acceptable to fetch all again?
                getVouchers();
            };
        }
        if (evt.target.className == "deleteButton") {
            if (window.confirm("Are you sure you want to permanently REMOVE this voucher?")) {
                await deleteVoucher(item.code);
                // TODO - acceptable to fetch all again?
                getVouchers();
            };
        }
    });
}

function translateUsedAvailable(used) {
    return used ? "no" : "yes";
}
