var username_box = document.getElementById("username_box")
var comment_box = document.getElementById("comment_box")

comment_box.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
	socket.emit('post_comment', {username:username_box.value, message:comment_box.value});
	comment_box.value="";
}

var chat_log = document.getElementById("chat_log");
socket.on('new_comment', function(comment_data){
	new_chat_row = document.createElement("tr");
	new_chat = document.createElement("td");
	username = document.createElement("span");
	separator = document.createElement("span");
	message = document.createElement("span");
	if (comment_data["username"]!==""){
		username.innerText=comment_data["username"];
	} else {
		username.innerText="Anonymous";
	}
	username.className = "Username" 
	separator.innerText=": ";
	message.innerText=comment_data["message"];
	new_chat.appendChild(username);
	new_chat.appendChild(separator);
	new_chat.appendChild(message);
	new_chat_row.appendChild(new_chat);
	chat_log.appendChild(new_chat_row);
});


