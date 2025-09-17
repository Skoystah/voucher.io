import { addVoucher, addVouchersFile } from "./api/vouchers.js";

const addVoucherSubmit = document.querySelector(".addVoucherSubmit");
addVoucherSubmit.addEventListener("click", async () => {

    const addVoucherResult = document.getElementById("addVoucherResult");
    addVoucherResult.textContent = '';
    addVoucherResult.style.display = 'none';

    const form = document.getElementById("vouchers-add-form");
    const formInput = new FormData(form);

    const inputCode = formInput.get("inputCode");
    const inputFile = formInput.get("file");

    if (inputFile.name) {
        if (inputCode) {
            addVoucherResult.style.color = "red";
            addVoucherResult.style.display = "block";
            addVoucherResult.textContent = 'Either add a file or add a code and duration';
        }
        else if (window.confirm("Are you sure you want to add vouchers from this file?")) {
            try {
                await addVouchersFile(formInput);
                await fillVoucherScreen();
                // TODO : feedback on which vouchers were added and which were not
                addVoucherResult.style.color = "green";
                addVoucherResult.style.display = "block";
                addVoucherResult.textContent = 'Successfully added vouchers!';
                form.reset();
            } catch (error) {
                addVoucherResult.style.color = "red";
                addVoucherResult.style.display = "block";
                addVoucherResult.textContent = error.message;
            }
        };
    } else {
        if (!inputCode) {
            addVoucherResult.style.color = "red";
            addVoucherResult.style.display = "block";
            addVoucherResult.textContent = 'Both code and duration need to be provided';
        }
        else if (window.confirm("Are you sure you want to add this voucher?")) {
            try {
                await addVoucher(formInput);
                await fillVoucherScreen();
                addVoucherResult.style.color = "green";
                addVoucherResult.style.display = "block";
                addVoucherResult.textContent = 'Successfully added voucher!';
                form.reset();
            } catch (error) {
                addVoucherResult.style.color = "red";
                addVoucherResult.style.display = "block";
                addVoucherResult.textContent = error.message;
            }
        };
    }
});

const voucherSearchForm = document.getElementById("vouchers-search-form");
voucherSearchForm.addEventListener("change", async (evt) => {
    if (evt.target.className === "filterVoucher") {
        await fillVoucherScreen();
    }
});
