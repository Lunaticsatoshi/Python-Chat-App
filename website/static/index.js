$(function () {
    $('#sendBtn').bind('click', function () {
        var value = document.getElementById("msg").value;
        $.getJSON('/send_messages',
            { val: value },
            function (data) {

            });
    });
});

window.addEventListener("load", function () {
    var update_loop = setInterval(update, 100);
    update();
});

function update() {
    fetch('/get_messages')
        .then(function (response) {
            return response.json();
        })
        .then(function (text) {
            console.log("run")
            var messages = "";
            for (value of text["messages"]){
                messages = messages + "<br >" + value
            }
            document.getElementById("test").innerHTML = messages;
        })
    return false;
}