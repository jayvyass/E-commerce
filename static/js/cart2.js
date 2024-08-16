// Function to get CSRF token from the meta tag
function getCSRFToken() {
    const tokenElement = document.querySelector('meta[name="csrf-token"]');
    return tokenElement ? tokenElement.getAttribute('content') : '';
}

// Alternative function to get CSRF token from cookies
function getCSRFTokenFromCookies() {
    const name = 'csrftoken=';
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}`);
    return parts.length === 2 ? parts.pop().split(';').shift() : '';
}

function updateCartQuantity(productId, change) {
    const cartItemRow = document.querySelector(`tr[data-product-id="${productId}"]`);
    if (!cartItemRow) return;
    const couponName = document.getElementById('coupon-name').value.trim();
    const quantityInput = cartItemRow.querySelector('.quantity-input');
    let currentQuantity = Number(quantityInput.value);
    let newQuantity = currentQuantity + change;

    // Ensure newQuantity is not less than zero
    if (newQuantity < 1) newQuantity = 1;

    // Temporarily update the quantity on the client-side
    quantityInput.value = newQuantity;

    // Calculate the new total price based on the new quantity
    const price = parseFloat(cartItemRow.querySelector('.price').textContent.replace('$', ''));
    const totalPrice = cartItemRow.querySelector('.total-price');
    totalPrice.textContent = `$${(price * newQuantity).toFixed(2)}`;

    // Update the cart with the new quantity on the server
    fetch('/update-cart-quantity/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            'product_id': productId,
            'quantity': newQuantity,
            'coupon_name': couponName
        })
    })
    .then(response => response.json())
    .then(data => handleUpdateCartResponse(data, quantityInput, totalPrice))
    .catch(error => console.error('Error updating cart quantity:', error));
}

function handleUpdateCartResponse(data, quantityInput, totalPrice) {
    if (data.success) {
        // Update the UI with the server response
        quantityInput.value = data.new_quantity;
        totalPrice.textContent = `$${data.new_total.toFixed(2)}`;

        // Update subtotal, discount, and total in the cart summary
        document.getElementById('subtotal').textContent = `$${data.new_subtotal.toFixed(2)}`;
        document.getElementById('discount').textContent = `$${data.discount_amount.toFixed(2)}`;
        document.getElementById('total').textContent = `$${data.new_total_with_shipping.toFixed(2)}`;
    } else {
        console.error('Error updating cart item:', data.error);
    }
}





// Function to apply a coupon
function applyCoupon() {
    const couponName = document.getElementById('coupon-name').value.trim();

    if (couponName === '') {
        Toastify({
            text: "Please enter a coupon code.",
            duration: 3000,
            gravity: "top",
            position: "right",
            backgroundColor: "#FFA500",
        }).showToast();
        return;
    }

    fetch('/apply-coupon/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFTokenFromCookies()
        },
        body: new URLSearchParams({ coupon_name: couponName })  // Send data as form-encoded
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text) });
        }
        return response.json();
    })
    .then(data => handleApplyCouponResponse(data))
    .catch(error => {
        console.error('Error applying coupon:', error);
        Toastify({
            text: "An error occurred while applying the coupon.",
            duration: 3000,
            gravity: "top",
            position: "right",
            backgroundColor: "#FF0000",
        }).showToast();
    });
}


// Handle response for applying a coupon
function handleApplyCouponResponse(data) {
    if (data.success) {
        const total = parseFloat(data.total);
        const discountAmount = parseFloat(data.discount_amount);

        if (!isNaN(total) && !isNaN(discountAmount)) {
            document.getElementById('total').textContent = `$${total.toFixed(2)}`;
            document.getElementById('discount').textContent = `$${discountAmount.toFixed(2)}`;
            Toastify({
                text: "Coupon applied Succesfully !",
                duration: 3000,
                gravity: "top",
                position: "right",
                backgroundColor: "#4CAF50",
                style: {
                    marginTop: "28px"  // Adjust the value as needed
                }
            }).showToast();
        } else {
            Toastify({
                text: "Invalid total or discount amount received.",
                duration: 3000,
                gravity: "top",
                position: "right",
                backgroundColor: "#FF0000",
            }).showToast();
        }
    } else {
        Toastify({
            text: data.message,
            duration: 3000,
            gravity: "top",
            position: "right",
            backgroundColor: "#FFA500",
        }).showToast();
    }
}

// Function to remove a cart item
function removeCartItem(productId) {
    const couponName = document.getElementById('coupon-name').value.trim();
    console.log("Removing item with product ID:", productId);
    fetch('/remove-cart-item/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            'product_id': productId,
            'coupon_name':couponName
        })
    })
    .then(response => response.json())
    .then(data => handleRemoveCartItemResponse(data, productId))
    .catch(error => {
        console.error('Error removing cart item:', error);
        alert('An error occurred while removing the item from the cart.');
    });
}

function handleRemoveCartItemResponse(data, productId) {
    if (data.success) {
        const cartItemRow = document.querySelector(`tr[data-product-id="${productId}"]`);
        if (cartItemRow) {
            cartItemRow.remove();
        }

        // Ensure the data fields are numbers
        const newSubtotal = parseFloat(data.new_subtotal);
        const discountAmount = parseFloat(data.discount_amount) || 0;
        const newTotalWithShipping = parseFloat(data.new_total_with_shipping);

        document.getElementById('subtotal').textContent = `$${newSubtotal.toFixed(2)}`;
        document.getElementById('discount').textContent = `$${discountAmount.toFixed(2)}`;
        document.getElementById('total').textContent = `$${newTotalWithShipping.toFixed(2)}`;
    } else {
        alert('Error removing item from cart');
    }
}

function proceedToCheckout() {
    // Get values from the DOM
    const subtotal = document.getElementById('subtotal').textContent.replace('$', '');
    const discount = document.getElementById('discount').textContent.replace('$', '');
    const total = document.getElementById('total').textContent.replace('$', '');

    // Store values in session storage
    sessionStorage.setItem('subtotal', subtotal);
    sessionStorage.setItem('discount', discount);
    sessionStorage.setItem('total', total);

    // Redirect to checkout page
    window.location.href = "{% url 'checkout' %}";
}
