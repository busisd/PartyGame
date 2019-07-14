var comment_box = document.getElementById("comment_box")

comment_box.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
	socket.emit('post_comment', {data: comment_box.value});
	comment_box.value="";
}


var newest_box = document.getElementById("newest_comment");
var chat_log = document.getElementById("chat_log");
socket.on('new_comment', function(msg){
	newest_box.innerText=msg;
	new_chat = document.createElement("div");
	new_chat.innerText=msg;
	chat_log.appendChild(new_chat);
});


