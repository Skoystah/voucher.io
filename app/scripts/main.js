import { API_URL } from "./config.js";

async function getVouchers() {
    const form = document.getElementById("vouchers-search-form");
    const formInput = new FormData(form);

    let params = new URLSearchParams();

    params.set("includeUsed", "false");
    for (const [key, value] of formInput) {
        switch (key) {
            case "duration":
                if (value.toLowerCase() === "any") {
                    break
                };
                params.set("duration", value);
                break;
            case "include-used":
                params.set("includeUsed", value);
                break;
        }
    }

    const query = params.toString();
    let url = base_url.concat("/vouchers")
    if (query) {
        url = url.concat("?", query);
    }

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        const data = await response.json()
        console.log(data);

        presentVouchers(data)
    } catch (error) {
        console.error(error.message);
    }
}

async function addVoucher() {
    const form = document.getElementById("vouchers-add-form");
    const formInput = new FormData(form);

    let url = base_url.concat("/vouchers")
    const request = new Request(
        url,
        {
            method: "POST",
            headers: { 'Content-Type': 'application/json', },
            body: JSON.stringify({
                code: formInput.get("inputCode"),
                duration: formInput.get("inputDuration"),
            }),
        }
    );

    try {
        const response = await fetch(request);
        if (!response.ok) {
            // if (response.status === 409) {
            const content = await response.json();
            throw new Error(content.detail);
            // throw new Error(`Response status: ${response.status}`);
            // };
        }
    } catch (error) {
        throw error;
    }
}
async function useVoucher(code) {
    console.log(`Using voucher ${code}`);

    let url = base_url.concat("/vouchers/", code)
    const request = new Request(
        url,
        {
            method: "PUT",
        }
    );

    try {
        const response = await fetch(request);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }
        // getVouchers();
    } catch (error) {
        console.error(error.message);
    }
}

async function deleteVoucher(code) {
    console.log(`Deleting voucher ${code}`);

    let url = base_url.concat("/vouchers/", code)
    const request = new Request(
        url,
        {
            method: "DELETE",
        }
    );

    try {
        const response = await fetch(request);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }
        // getVouchers();
    } catch (error) {
        console.error(error.message);

    }
}

function translateUsedAvailable(used) {
    return used ? "no" : "yes";
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
            useButton.textContent = "Use voucher";
            useButton.addEventListener("click", async () => {
                if (window.confirm("Are you sure you want to use this voucher?")) {
                    await useVoucher(item.code);
                    // TODO - acceptable to fetch all again?
                    getVouchers();
                };
            });
            voucherTableRow.appendChild(useButton);
        } else {
            const deleteButton = document.createElement("button");
            deleteButton.textContent = "Remove voucher";
            deleteButton.addEventListener("click", async () => {
                if (window.confirm("Are you sure you want to permanently REMOVE this voucher?")) {
                    await deleteVoucher(item.code);
                    // TODO - acceptable to fetch all again?
                    getVouchers();
                };
            });
            voucherTableRow.appendChild(deleteButton);
        }
    }
}

const addVoucherSubmit = document.querySelector(".addVoucherSubmit");
addVoucherSubmit.addEventListener("click", async () => {


    const addVoucherResult = document.getElementById("addVoucherResult");
    addVoucherResult.textContent = '';
    addVoucherResult.style.display = 'none';

    if (window.confirm("Are you sure you want to add this voucher?")) {
        try {
            await addVoucher();
            getVouchers();
        } catch (error) {
            addVoucherResult.style.color = "red";
            addVoucherResult.style.display = "block";
            addVoucherResult.textContent = error.message;
        }
    };
});

const changeFilters = document.querySelectorAll(".filterVoucher");
for (const filter of changeFilters) {
    filter.addEventListener("change", () => {
        getVouchers();
    });
}

// TODO - ENV VARIABLE
const base_url = API_URL;

// ON LOADING
getVouchers();
