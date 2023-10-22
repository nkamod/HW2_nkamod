function getShowTimes(selectedDate) {
    event.preventDefault();

    $.ajax({
        type: 'GET',
        url: window.location.href,
        data: { selected_date: selectedDate },
        success: function(response) {

            const stw = document.getElementById("show-times-wrapper");
            stw.innerHTML = "";

            $(".btn-date.active").removeClass("active");
            $(`.btn-date:contains('${selectedDate}')`).addClass("active");

            response.shows.forEach(show => {
                const button = document.createElement("a");
                button.href = "/show/" + show.pk;
                button.classList.add("btn");
                button.classList.add("btn-time")
                button.innerText = `${show.hour}:${show.minute}`;
                stw.appendChild(button);
            });

        },
        error: function(error) {
            console.error(error);
        }
    });
}