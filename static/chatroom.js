var socket = io();
socket.on('connect', function() {
	socket.emit('connection_event');
});


var comment_box = document.getElementById("comment_box")

comment_box.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
	if (comment_box.value!==""){
		socket.emit('post_comment', {message:comment_box.value});
		comment_box.value="";
	}
}


/*
Keeps scroll box scrolled to the bottom
*/
var chat_log_div = document.getElementById("chat_log_div");
function checkShouldScroll(){
	return (chat_log_div.offsetHeight+chat_log_div.scrollTop+1 >= chat_log_div.scrollHeight)
}

function updateScroll(){
    chat_log_div.scrollTop = chat_log_div.scrollHeight;
}

var chat_log = document.getElementById("chat_log");
socket.on('new_comment', function(comment_data){
	var shouldScroll = checkShouldScroll();
	// console.log(chat_log_div.offsetHeight+chat_log_div.scrollTop)
	// console.log(chat_log_div.scrollHeight)
	
	new_chat_row = document.createElement("tr");
	new_chat_row.className = "chatmessage";
	new_chat = document.createElement("td");
	username = document.createElement("span");
	username.className = "Username";
	separator = document.createElement("span");
	separator.className = "Separator";
	message = document.createElement("span");
	message.className = "Message";
	if (comment_data["username"]!==""){
		username.innerText=comment_data["username"];
	} else {
		username.innerText="Anonymous";
	}
	separator.innerText=": ";
	message.innerText=comment_data["message"];
	new_chat.appendChild(username);
	new_chat.appendChild(separator);
	new_chat.appendChild(message);
	new_chat_row.appendChild(new_chat);
	chat_log.appendChild(new_chat_row);
	
	if (shouldScroll) {
		updateScroll();
	}
	
	if (comment_data['cur_row'] !== null && comment_data['cur_col'] !== null) {
		popUpMessage(comment_data);
	}
});

socket.on('new_user_connected', function(userDict){
	var shouldScroll = checkShouldScroll();	new_chat_row = document.createElement("tr");
	new_chat_row.className = "newuser"
	new_chat = document.createElement("td");
	username = document.createElement("span");
	username.className = "Username";
	message = document.createElement("span");
	message.className = "Message";
	username.innerText=userDict["username"];
	message.innerText=" has connected!";
	new_chat.appendChild(username);
	new_chat.appendChild(message);
	new_chat_row.appendChild(new_chat);
	chat_log.appendChild(new_chat_row);
	
	if (shouldScroll) {
		updateScroll();
	}
	
	if (userDict['cur_row'] !== null && userDict['cur_col'] !== null) {
		draw_stickman(userDict['cur_row'], userDict['cur_col']);
	}
});

chat_map = document.getElementById("chat_map");
for (i=0; i<chat_map.children[0].children.length; i++){
	for (j=0; j<chat_map.children[0].children[i].children.length; j++){
		nums = [String(Math.random()*255), String(Math.random()*255), String(Math.random()*255)];
		chat_map.children[0].children[i].children[j].style.backgroundColor="rgba("+nums[0]+","+nums[1]+","+nums[2]+", .2)";
		chat_map.children[0].children[i].children[j].id = "chat_map_"+i.toString()+"_"+j.toString()
	}
}

function popUpMessage(comment_data){
	console.log(comment_data);
	chatter_div = document.getElementById("chat_map_"+comment_data["cur_row"].toString()+"_"+comment_data["cur_col"].toString());
	var rect = chatter_div.getBoundingClientRect();
	var chat_box = document.createElement("div");
	var chat_par = document.createElement("p");
	chat_box.className = "chat_box";
	chat_box.style.top = (rect.top-50+25).toString()+"px";
	chat_box.style.left = (rect.right-25).toString()+"px";
	chat_par.innerText = comment_data["message"];
	chat_par.style.overflowY = "hidden";
	chat_par.style.maxHeight = "-webkit-fill-available";
	chat_par.style.margin = "0px";
	chat_box.appendChild(chat_par);
	document.body.appendChild(chat_box);
		
	setTimeout(function() {
		document.body.removeChild(chat_box);
	}, 4200);
}

function moveStickman(direction){
	socket.emit('move_stickman', direction);
}

socket.on('stickman_moved', function(stickman_pos_data) {
	erase_stickman(stickman_pos_data['old_row'], stickman_pos_data['old_col']);
	draw_stickman(stickman_pos_data['new_row'], stickman_pos_data['new_col']);
});

function draw_stickman(row, col) {
	chat_map.children[0].children[row].children[col].style.backgroundImage = "url(static/stickman.png)";
}

function erase_stickman(row, col) {
	chat_map.children[0].children[row].children[col].style.backgroundImage = "";
}
