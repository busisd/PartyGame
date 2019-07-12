import flask
import time
import json


app = flask.Flask(__name__)
start_time = -999999



@app.route('/')
def main_page():
	uptime = round(time.time() - start_time)
	site_url = flask.request.base_url
	return flask.render_template('homepage.html', uptime = uptime, site_url = site_url)

@app.route('/json_data')
def json_data():
	return json.dumps(['a', 'b', 'c'])


if __name__ == '__main__':
	start_time = time.time()
	app.run(host='localhost', port=5555, threaded=True)
	

