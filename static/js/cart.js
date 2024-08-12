   // Function to get CSRF token from the meta tag
   function getCSRFToken() {
    const tokenElement = document.querySelector('meta[name="csrf-token"]');
    return tokenElement ? tokenElement.getAttribute('content') : '';
}


function updateCartQuantity(productId, change) {
    // Get the current quantity input element
    const cartItemRow = document.querySelector(`tr[data-product-id="${productId}"]`);
    if (cartItemRow) {
        const quantityInput = cartItemRow.querySelector('.quantity-input');
        let currentQuantity = Number(quantityInput.value);
        let newQuantity = currentQuantity + change;

        // Ensure newQuantity is not less than zero
        if (newQuantity < 0) newQuantity = 0;

        // Temporarily update the quantity on the client-side
        quantityInput.value = newQuantity;

        // Calculate the new total price based on the new quantity
        const price = parseFloat(cartItemRow.querySelector('.price').textContent.replace('$', ''));
        const totalPrice = cartItemRow.querySelector('.total-price');
        totalPrice.textContent = `$${(price * newQuantity).toFixed(2)}`;

        // Update the cart with the new quantity
        fetch('/update-cart-quantity/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()  // Ensure CSRF token is included
            },
            body: JSON.stringify({
                'product_id': productId,
                'quantity': newQuantity
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Correct the UI with the actual server response
                const newQuantity = Number(data.new_quantity);
                const newTotal = Number(data.new_total);
                const newSubtotal = Number(data.new_subtotal);
                const discountAmount = Number(data.discount_amount);
                const newTotalWithShipping = Number(data.new_total_with_shipping);

                // Update the UI with the server response
                quantityInput.value = newQuantity;
                totalPrice.textContent = `$${newTotal.toFixed(2)}`;

                // Update subtotal, discount, and total in the cart summary
                document.getElementById('subtotal').textContent = `$${newSubtotal.toFixed(2)}`;
                document.getElementById('discount').textContent = `$${discountAmount.toFixed(2)}`;
                document.getElementById('total').textContent = `$${newTotalWithShipping.toFixed(2)}`;
            } else {
                console.error('Error updating cart item');
            }
        })
        .catch(error => console.error('Error:', error));
    }
}



function getCSRFToken2() {
    const name = 'csrftoken=';
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function applyCoupon() {
    const couponName = document.getElementById('coupon-name').value;

    fetch('/apply-coupon/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken2()
        },
        body: new URLSearchParams({ coupon_name: couponName })  // Send data as form-encoded
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text) });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Ensure data.total and data.discount_amount are treated as numbers
            let total = parseFloat(data.total);
            let discountAmount = parseFloat(data.discount_amount);
            
            if (!isNaN(total) && !isNaN(discountAmount)) {
                document.getElementById('total').textContent = `$${total.toFixed(2)}`;
                document.getElementById('discount').textContent = `$${discountAmount.toFixed(2)}`;  // Add this line to update discount amount
                alert('Coupon applied successfully!');
            } else {
                alert('Invalid total or discount amount received.');
            }
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while applying the coupon.');
    });
}

