'use strict';
const stripe = Stripe(STRIPE_PUBLISHABLE_KEY);
const elem = document.getElementById('submit');
const clientsecret = elem.getAttribute('data-secret');

// Set up Stripe.js and Elements to use in checkout form
const elements = stripe.elements();
const style = {
base: {
  color: "#000",
  lineHeight: '2.4',
  fontSize: '16px'
}
};


var card = elements.create("card", { style: style });
card.mount("#card-element");

card.on('change', function(event) {
var displayError = document.getElementById('card-errors')
if (event.error) {
  displayError.textContent = event.error.message;
  $('#card-errors').addClass('alert alert-info');
} else {
  displayError.textContent = '';
  $('#card-errors').removeClass('alert alert-info');
}
});

var form = document.getElementById('payment-form');

form.addEventListener('submit', async function(ev) {
ev.preventDefault();

var custName = document.getElementById("custName").value;
var custAdd = document.getElementById("custAdd").value;
var custAdd2 = document.getElementById("custAdd2").value;
var postCode = document.getElementById("postCode").value;
 

const req = fetch('http://127.0.0.1:8000/orders/add/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': CSRF_TOKEN
    },
    body: JSON.stringify({
      order_key: clientsecret,
      csrfmiddlewaretoken: CSRF_TOKEN,
      action: "post",
    }),
  })
  const response = await req 
  const body = await response.json() 
  if (response.ok) {
    // Handle success 
    stripe.confirmCardPayment(clientsecret, {
      payment_method: {
        card: card,
        billing_details: {
          address:{
              line1:custAdd,
              line2:custAdd2
          },
          name: custName
        },
      }
    }).then(function(result) {
        if (result.error) {
                console.log('payment error', result.error)
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                document.cookie = "payment=success;path=/;";
                window.location.replace(`http://127.0.0.1:8000/payment/${body.product_id}/order_succeeded/`);
            } 
        }
    })
  } else {
    // Handle error
    console.log('error')
  }

 
});

