// Add event listeners to the 'update-cart' buttons
var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'Action:', action);
        console.log('USER:', user);

        if (user === 'AnonymousUser') {
            var csrftoken = getCookie('csrftoken');
            addCookieItem(productId, action, csrftoken);
        } else {
            updateUserOrder(productId, action);
        }
    });
}

function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data...');

    var url = '/update_item/';
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        location.reload();
    });
}

function addCookieItem(productId, action, csrftoken) {
    console.log('User is not authenticated');

    if (action === 'add') {
        if (cart[productId] === undefined) {
            cart[productId] = { 'quantity': 1 };
        } else {
            cart[productId]['quantity'] += 1;
        }
    }

    if (action === 'remove') {
        cart[productId]['quantity'] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            console.log('Item should be deleted');
            delete cart[productId];
        }
    }

    console.log('CART:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + '; domain=; path=/';
    location.reload();
}

function getCookie(name) {
    // Padalina slapuku eilute ir gauna visas atskiras vardas = vertes poras masyve
    var cookieArr = document.cookie.split(";");

    // Pereina per masyvo elementus
    for(var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");


        if(name == cookiePair[0].trim()) {
            // Issifruoja slapuko verte ir grazina
            return decodeURIComponent(cookiePair[1]);
        }
    }

    // grazina 0 jei nieko neranda grazina nuline reiksme
    return null;
}
