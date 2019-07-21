import flask
import time
import json
from flask_socketio import SocketIO
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

app = flask.Flask(__name__)
app.config.from_object('testsite_config')
socketio = SocketIO(app)

#db.execute("CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL);")
def get_db():
	if 'db' not in flask.g:
		flask.g.db = sqlite3.connect('chat_db')
		flask.g.db.row_factory = sqlite3.Row
	return flask.g.db
	
def close_db(e = None):
	db = flask.g.pop('db', None)
	if db is not None:
		db.close()
app.teardown_appcontext(close_db)


start_time = -999999
@app.route('/')
def main_page():
	return flask.redirect(flask.url_for('chatroom'))
	# uptime = round(time.time() - start_time)
	# site_url = flask.request.base_url
	# return flask.render_template('homepage.html', uptime = uptime, site_url = site_url)

@app.route('/json_data')
def json_data():
	return json.dumps(['a', 'b', 'c'])

@app.route('/chatroom', methods=('GET', 'POST'))
def chatroom():
	if flask.request.method=='GET':
		return flask.render_template('chatroom.html')
	elif flask.request.method=='POST':
		print('Form received', str(flask.request.form))
		return 'Success'

@app.route('/login', methods=['GET', 'POST'])
def login():
	if flask.request.method == "POST":
		username = flask.request.form.get('username', None)
		password = flask.request.form.get('password', None)
		
		db = get_db()
		cur_user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
		
		error = None
		if cur_user is None:
			error = "Username does not exist!"
		elif not check_password_hash(cur_user['password'], password):
			error = "Incorrect password."
		
		if error is not None:
			flask.flash(error)
			return flask.render_template('chat_login.html')
		else:
			flask.session.clear()
			flask.session['cur_user_id'] = cur_user['id']
			return flask.redirect(flask.url_for('chatroom'))
	else:
		return flask.render_template('chat_login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if flask.request.method == "POST":
		new_username = flask.request.form.get("username", None)
		new_password = flask.request.form.get("password", None)
		new_password_confirm = flask.request.form.get("password_confirm", None)
		
		db = get_db()
		
		error = None
		if new_username is None or len(new_username) < 3:
			error = "Username must be at least 3 letters long!"
		elif new_password is None or len(new_password) < 6:
			error = "Password must contain at least 6 characters!"
		elif new_password != new_password_confirm:
			error = "Password and confirmation did not match, please try again."
		elif db.execute('SELECT id FROM user WHERE username = ?', (new_username,)).fetchone() is not None:
			error = "An account with that username already exists. Please choose a different username."
			
		if error is not None:
			flask.flash(error)
			return flask.render_template('chat_register.html')
		else:
			db.execute(
				'INSERT INTO user (username, password) VALUES (?,?)', 
				(new_username, generate_password_hash(new_password))
			)
			db.commit()
			return flask.redirect(flask.url_for('login'))
	else:
		return flask.render_template('chat_register.html')

@app.route('/logout')
def logout():
	flask.session.clear()
	return flask.redirect(flask.url_for('chatroom'))

@socketio.on('message')
def handle_message(message):
	print('received message: ' + message)

@socketio.on('json')
def handle_json(json):
	print('received json: ' + str(json))

@socketio.on('my event')
def handle_my_custom_event(json, string_data):
	print('received custom event:', str(json), string_data)

@socketio.on('post_comment')
def handle_comment(comment_data):
	# print('Comment posted: '+str(comment_data['message']))
	# print('Session ID:', flask.request.sid) #Session ID changes on page refresh
	# print("\n"+str(flask.session.get('cur_user_id', "No user specified!"))+"\n") #Prints the current user id
	cur_id = flask.session.get('cur_user_id', None)
	if cur_id is not None:
		db = get_db()
		user = db.execute("SELECT * FROM user WHERE id = ?", (cur_id,)).fetchone()
		username = user['username']
		comment_data['username'] = username
	else:
		comment_data['username'] = "Anonymous"
		
	if len(comment_data["message"]) > 500:
		comment_data["message"] = comment_data["message"][0:500]
	
	socketio.emit('new_comment', comment_data)

# def verify_user(username, password_hash):
	# '''
	# This method is kind of bad because someone could be 
	# impersonated using only their password hash
	# '''
	# db = get_db()
	# user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
	# if user is None:
		# return False
	# return password_hash == user["password"]

def pass_user():
	cur_user_id = flask.session.get('cur_user_id', None)
	if cur_user_id is None:
		flask.g.cur_user = None
	else:
		db = get_db()
		cur_user = db.execute('SELECT * FROM user WHERE id = ?', (cur_user_id,)).fetchone()
		flask.g.cur_user = cur_user
app.before_request(pass_user)

if __name__ == '__main__':
	start_time = time.time()
	# app.run(host='localhost', port=5555, threaded=True)
	socketio.run(app, host='0.0.0.0', port=1203)


