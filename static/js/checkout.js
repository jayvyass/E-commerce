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
                        if (data.errors) {
                            displayFormErrors(data.errors);
                        }
                        throw new Error('Form validation failed.');
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
                }
            })
            .catch(error => {
                console.error('Error:', error);
                Toastify({
                    text: 'An error occurred. Please try again.',
                    duration: 5000,
                    backgroundColor: 'linear-gradient(to right, #FF5F6D, #FFC371)',
                    close: true
                }).showToast();
            });
        },
        onApprove: function (data, actions) {
            return actions.order.capture().then(function (details) {
              
                Toastify({
                    text: 'Transaction completed by ' + details.payer.name.given_name,
                    duration: 5000,
                    backgroundColor: 'linear-gradient(to right, #00b09b, #96c93d)',
                    close: true
                }).showToast();
                // Redirect to the success page or perform any additional actions
                window.location.href = '/';// Change to your success page URL
            });
        },
        onError: function(err) {
            console.error('PayPal checkout error', err);
            Toastify({
                text: 'An error occurred with PayPal Checkout. Please try again.',
                duration: 5000,
                backgroundColor: 'linear-gradient(to right, #FF5F6D, #FFC371)',
                close: true
            }).showToast();
        }
    }).render('#paypal-button-container');
}


// Function to display form validation errors
// Function to display form validation errors
function displayFormErrors(errors) {
    // Clear previous error messages
    document.querySelectorAll('.form-error').forEach(function(el) {
        el.remove();
    });

    for (let field in errors) {
        if (errors.hasOwnProperty(field)) {
            const errorMessages = errors[field].join(' ');
            const inputField = document.querySelector(`[name="${field}"]`);
            if (inputField) {
                let errorElement = document.createElement('div');
                errorElement.className = 'form-error text-danger';
                errorElement.textContent = `Error in ${field.replace(/([A-Z])/g, ' $1')}: ${errorMessages}`;
                inputField.parentNode.insertBefore(errorElement, inputField.nextSibling);  
            }
        }
    }
}

// Render PayPal button on page load
renderPaypalButton();
