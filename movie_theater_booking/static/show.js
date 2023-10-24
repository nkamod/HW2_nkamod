let totalPrice = 0;

function seatSelected(seat, price) {

    if (!$(`#${seat}`).prop("checked")) {
        const pList = document.getElementById("seats-selected").getElementsByTagName("p");
        for (let p of pList) {
            if (p.innerText === `${seat} - $${price}`) {
                p.parentNode.removeChild(p);
            }
        }

        totalPrice -= parseFloat(price);
    } else {
        const p = document.createElement("p");
        p.classList.add("m-0");
        p.classList.add("text-white");
        p.innerText = `${seat} - \$${price}`;

        document.getElementById("seats-selected").appendChild(p);
        totalPrice += parseFloat(price);
    }

    document.getElementById("btn-book").innerText = `Book @ $${totalPrice}`;

}

function bookTicket(pk) {

    selectedSeats = [];
    $("#seat-config input[type='checkbox']").each(function() {
        if ($(this).is(":checked")) {
            selectedSeats.push($(this).attr("id"));
        }
    });

    const csrftoken = getCookie('csrftoken');

    $.ajax({
        type: 'POST',
        url: '/book_show',
        data: JSON.stringify({ pk: pk, selectedSeats: selectedSeats }),
        contentType: 'application/json',
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        success: function(response) {

            const popup = $("#pop-up");

            popup.removeClass("d-none");

            popup.addClass("d-flex");
            
            // if (response.redirect) {
            //     const baseUrl = window.location.protocol + "//" + window.location.host;
            //     window.location.href = baseUrl + "/" + response.redirect;
            // } else {
            //     console.log(response);
            // }

        },
        error: function(error) {
            console.error('Error:', error);
        }
    });

}

// Function to get the CSRF token from the cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}