
document.addEventListener("DOMContentLoaded", function () {

    /* =============================
       BOOKING PAGE LOGIC
    ============================== */
    const bookingForm = document.getElementById("bookingForm");

    if (bookingForm) {

        const destination = document.getElementById("destination");
        const contact = document.getElementById("contact");
        const packageSelect = document.getElementById("package");
        const adults = document.getElementById("adultsInput");
        const children = document.getElementById("childrenInput");
        const totalPrice = document.getElementById("total_price");

        function calculateTotal() {
            const basePrice = parseInt(
                destination.options[destination.selectedIndex]?.dataset.price
            ) || 0;

            const adultCount = parseInt(adults.value) || 0;
            const childCount = parseInt(children.value) || 0;

            const multiplier = parseFloat(
                packageSelect.options[packageSelect.selectedIndex]?.dataset.mult
            ) || 1;

            const total =
                (adultCount * basePrice) +
                (childCount * (basePrice / 2));

            totalPrice.value = Math.round(total * multiplier);
        }

        destination.addEventListener("change", calculateTotal);
        packageSelect.addEventListener("change", calculateTotal);
        adults.addEventListener("input", calculateTotal);
        children.addEventListener("input", calculateTotal);

        calculateTotal();

        bookingForm.addEventListener("submit", function (e) {
            e.preventDefault();

            if (!contact.value.trim()) {
                alert("Please enter contact number");
                return;
            }

            const formData = new URLSearchParams();
            formData.append("name", document.getElementById("nameInput").value);
            formData.append("destination", destination.value); // ✅ FIX
            formData.append("contact", contact.value);
            formData.append("package", packageSelect.value);
            formData.append("adults", adults.value);
            formData.append("children", children.value);
            formData.append("date", document.getElementById("dateInput").value);
            formData.append("total_price", totalPrice.value);

            fetch("/booking/save", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: formData.toString()
            })
            .then(res => {
                if (!res.ok) throw new Error("Booking failed");
                return res.text();
            })
            .then(() => {
                alert("Booking saved successfully!");
                window.location.href = "/history";
            })
            .catch(err => {
                console.error(err);
                alert("Booking failed! Check backend route.");
            });
        });
    }

    /* =============================
       ADMIN BOOKING PAGE
    ============================== */
    const bookingTable = document.getElementById("bookingTable");

    if (bookingTable) {

        const searchInput = document.getElementById("searchInput");

        if (searchInput) {
            searchInput.addEventListener("keyup", function () {
                const filter = this.value.toLowerCase();
                bookingTable.querySelectorAll("tbody tr").forEach(row => {
                    row.style.display = row.innerText
                        .toLowerCase()
                        .includes(filter)
                        ? ""
                        : "none";
                });
            });
        }

        document.querySelectorAll(".delete-booking").forEach(btn => {
            btn.addEventListener("click", function () {
                if (!confirm("Delete this booking?")) return;

                fetch(`/admin/booking/delete/${this.dataset.id}`, {
                    method: "DELETE"
                }).then(res => {
                    if (res.ok) location.reload();
                });
            });
        });
    }

    /* =============================
       ADMIN DESTINATION DELETE + SEARCH
    ============================== */

    document.querySelectorAll(".btn-delete").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            if (!confirm("Delete this destination?")) return;
            this.closest("form").submit();
        });
    });

    const searchInputDest = document.getElementById("searchInputDest");
    const tableBody = document.querySelector("#destinationTable tbody");

    if (searchInputDest && tableBody) {
        searchInputDest.addEventListener("keyup", function () {
            const filter = this.value.toLowerCase();
            tableBody.querySelectorAll("tr").forEach(row => {
                row.style.display =
                    row.innerText.toLowerCase().includes(filter)
                        ? ""
                        : "none";
            });
        });
    }
});