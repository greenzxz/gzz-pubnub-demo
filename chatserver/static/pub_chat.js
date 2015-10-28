(function(){

var box = PUBNUB.$('box'), input = PUBNUB.$('input'), channel = 'gzz-demo-chat';

PUBNUB.subscribe({
    channel  : channel,
    callback : function(text) {
        box.innerHTML = (''+channel).replace( /[<>]/g, '' ) + ': ' +
                        (''+text).replace( /[<>]/g, '' ) + '<br />' + box.innerHTML
                        }
});
PUBNUB.bind( 'keyup', input, function(e) {
    (e.keyCode || e.charCode) === 13 && PUBNUB.publish({
        channel : channel, message : input.value, x : (input.value='')
    })
} );

})()