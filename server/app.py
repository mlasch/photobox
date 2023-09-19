from flask import Flask, render_template, Response

from eventqueue import EventQueue
import subprocess
app = Flask(__name__)
announcer = EventQueue()


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/photo', methods=['POST'])
def photo():
    stdout = subprocess.check_output(["sh", "gphoto_dummy.sh"])
    announcer.announce(msg=stdout.decode())
    return {}, 200


@app.route('/listen', methods=['GET'])
def listen():
    print("Start Listen")

    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            print("yield message", msg)
            yield f"data: {msg}\n\n"

    return Response(stream(), mimetype='text/event-stream')
