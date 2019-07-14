import flask
import time
import json
from flask_socketio import SocketIO

app = flask.Flask(__name__)
app.config['SECRET-KEY'] = 'secretsecret'
socketio = SocketIO(app)

start_time = -999999

users_in_game = []
#make a page where people can register themselves into the game with a unique nickname
#then have the server return diffferent pages at /game given the status of the participants in each section
#also keep track of the 'ready' status of each user
#if the majority of users are ready, then remaining users have 30 seconds to enter their answers or they 
#are either kicked or get a default answers
#might make more sense to just make a chatroom to get 2-way connection? then use that


@app.route('/')
def main_page():
	uptime = round(time.time() - start_time)
	site_url = flask.request.base_url
	return flask.render_template('homepage.html', uptime = uptime, site_url = site_url)

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

@socketio.on('message')
def handle_message(message):
	print('received message: ' + message)

@socketio.on('json')
def handle_json(json):
	print('received json: ' + str(json))

@socketio.on('my event')
def handle_my_custom_event(json, string_data):
	print('received custom event: ' + str(json) + string_data)

@socketio.on('post_comment')
def handle_my_custom_event(comment_data):
	print('Comment posted: '+str(comment_data['data']))
	socketio.emit('new_comment', str(comment_data['data']))

if __name__ == '__main__':
	start_time = time.time()
	# app.run(host='localhost', port=5555, threaded=True)
	socketio.run(app, host='localhost', port=5555)


