$(document).ready(function() {
    var startButton = $("#startChatButton"),
        username = '',
        channel_name = ''


        usernameInput = $('#username'),
        pages = {
            login: $("#loginPage"),
            chat: $("#chatPage"),
        };

    function httpPostAsync(theUrl, callback, payload) {

        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        function formatParams(param_object) {
            var params = ""
            for (var key in param_object) {
                if (param_object.hasOwnProperty(key)) {
                    params += key + '=' + param_object[key] + "&"
                }
            }
            return params;
        }


        var http_req = new XMLHttpRequest();
        http_req.onreadystatechange = function () {
            if (http_req.readyState == 4 && http_req.status == 200)
                callback(http_req.responseText);
        }

        http_req.open("POST", theUrl, true);
        http_req.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));


        var params = formatParams(payload);
        http_req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        http_req.setRequestHeader("Content-length", params.length);
        http_req.setRequestHeader("Connection", "close");

        http_req.send(params);
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

    ///// LoginView
    function LoginView() {
        clearAll();
        document.getElementById("loginPage").style.display="inherit";
        startButton.off('click');
        startButton.click(function (event) {
          if(usernameInput.val() != '') {
            username = usernameInput.val();
            chatView()
          }
        });
    }

    function chatView() {
        clearAll();

        document.getElementById("chatPage").style.display="inherit";

        document.getElementById("SplashWelcome").innerHTML =
            "Welcome, " + username + ", to our simple pubnub chat.<br />"

        function loadChannel() {
            function loadChannelCallback(text) {
                console.log(text)
                var json_out = JSON.parse(text);
                document.getElementById("channel_name").innerHTML = "<b>" + json_out['channel'] + "</b>";

                start_chatting(json_out.channel, json_out.subscribe_key, json_out.publish_key);
            }

            httpGetAsync('/chat/get_keys', loadChannelCallback);
        }
        function start_chatting(channel_name, subscribe_key, publish_key) {
            var pubnub_conn = PUBNUB.init({
                publish_key: publish_key,
                subscribe_key: subscribe_key
            });

            var box = PUBNUB.$('box'), input = PUBNUB.$('input');

            function handle_message(message) {
                if (message.msg_type == 'alert') {
                    PUBNUB.$('alert').innerHTML = "<b>" + ('' + message.text).replace( /[<>]/g, '' ) + "</b>";
                    return;
                }
                else {
                    PUBNUB.$('alert').innerHTML = "";
                }
                box.innerHTML = (''+message.user).replace( /[<>]/g, '' ) + ': ' +
                                (''+message.text).replace( /[<>]/g, '' ) + '<br />' + box.innerHTML;

            };

            function new_message(event) {
                if ((event.keyCode || event.charCode) === 13) {
                    httpPostAsync('/chat/send_msg', function(resp) {}, {
                        'user': username,
                        'text': input.value,
                        'x' : (input.value=''),
                    });
                }
            };

            PUBNUB.bind('keyup', input, new_message);
            pubnub_conn.subscribe( {
                channel: channel_name,
                message: handle_message
            });
        }
        loadChannel();
    }

    function clearAll() {
        document.getElementById("loginPage").style.display="none";
        document.getElementById("chatPage").style.display="none";
    }

    LoginView();

});