(function () {
    function httpPostAsync(theUrl, callback, payload) {
        var http_req = new XMLHttpRequest();
        http_req.onreadystatechange = function () {
            if (http_req.readyState == 4 && http_req.status == 200)
                callback(http_req.responseText);
        }

        http_req.open("POST", theUrl, true);
        http_req.send(payload);
    }

    function httpGetAsync(theUrl, callback) {
        var http_req = new XMLHttpRequest();
        http_req.onreadystatechange = function () {
            if (http_req.readyState == 4 && http_req.status == 200)
                callback(http_req.responseText);
        }

        http_req.open("GET", theUrl, true);
        http_req.send();
    }

    function loadChannel() {
        function loadChannelCallback(text) {
            var json_out = JSON.parse(text);
            document.getElementById("channel_name").innerHTML = "<b>" + json_out['channel'] + "</b>";
        }

        httpGetAsync('/chat/login', loadChannelCallback);
    }

    loadChannel();
})();