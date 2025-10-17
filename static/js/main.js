// Simple JS for product card hover effects or dynamic filtering
document.addEventListener("DOMContentLoaded", function() {
    const filterForm = document.querySelector(".filter-form");
    if(filterForm) {
        filterForm.addEventListener("submit", function() {
            console.log("Filters applied!");
        });
    }

    const addBtns = document.querySelectorAll(".add-btn");
    addBtns.forEach(btn => {
        btn.addEventListener("click", function(e) {
            e.preventDefault();
            alert("Product added to cart!");
            window.location.href = this.href; // redirect after alert
        });
    });
});

