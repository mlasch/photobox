import flask

from eventqueue import EventQueue

app = flask.Flask(__name__)
announcer = EventQueue


@app.route('/')
def hello_world():
    return "Hello World!"


@app.route('/listen', methods=['GET'])
def listen():

    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return flask.Response(stream(), mimetype='text/event-stream')
