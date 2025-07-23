async function getVouchers() {
    const url = "http://localhost:8000/vouchers";
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

async function useVoucher(code) {
    console.log(`Using voucher ${code}`);

    const url = `http://localhost:8000/vouchers/${code}`;
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

        const data = await response.json()
        console.log(data);

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
            useButton.addEventListener("click", () => {
                useVoucher(item.code);
                //TODO - get updated resource from API?
                item.used = true;
                availableData.textContent = translateUsedAvailable(item.used);
                voucherTableRow.removeChild(useButton);
            });
            voucherTableRow.appendChild(useButton);
        }
    }
}

const getVoucherSubmit = document.querySelector(".getVoucherSubmit");
getVoucherSubmit.addEventListener("click", getVouchers);


