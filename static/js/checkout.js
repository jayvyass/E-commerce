document.addEventListener('DOMContentLoaded', function() {
    // Retrieve values from session storage
    const subtotal = sessionStorage.getItem('subtotal') || '0.00';
    const discount = sessionStorage.getItem('discount') || '0.00';
    const total = sessionStorage.getItem('total') || '0.00';

    // Update the HTML elements with these values
    document.getElementById('subtotal').textContent = `$${parseFloat(subtotal).toFixed(2)}`;
    document.getElementById('discount').textContent = `$${parseFloat(discount).toFixed(2)}`;
    document.getElementById('total').textContent = `$${parseFloat(total).toFixed(2)}`;

    // Set the value of the hidden amount input field
    document.getElementById('amount').value = parseFloat(total).toFixed(2);
});

// Function to render PayPal button
function renderPaypalButton() {
    paypal.Buttons({
        style: {
            color: 'blue',
            shape: 'rect',
            label: 'pay',
            height: 50
        },
        createOrder: function (data, actions) {
            const form = document.getElementById('checkout-form');
            const formData = new FormData(form);

            // Submit form data to the server first
            return fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.errors ? JSON.stringify(data.errors) : 'Form submission failed');
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Proceed with PayPal payment
                    const totalPrice = document.getElementById('total').textContent.replace('$', '').trim();
                    return actions.order.create({
                        purchase_units: [{
                            amount: {
                                value: totalPrice
                            }
                        }]
                    });
                } else {
                    console.error('Form validation errors:', data.errors);
                    alert('Form validation failed. Please check your input.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        },
        onApprove: function (data, actions) {
            return actions.order.capture().then(function (details) {
                alert('Transaction completed by ' + details.payer.name.given_name);

                // Redirect to the success page or perform any additional actions
                window.location.href = '/'; // Change to your success page URL
            });
        },
        onError: function(err) {
            console.error('PayPal checkout error', err);
            alert('An error occurred with PayPal Checkout. Please try again.');
        }
    }).render('#paypal-button-container');
}

// Render PayPal button on page load
renderPaypalButton();
