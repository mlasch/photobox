import queue
import subprocess
from queue import Queue
from threading import Thread

from flask import Flask, Response, render_template

from eventqueue import EventQueue


def threaded_task(photo_event, announcer):
    while True:
        photo_event.get()
        stdout = subprocess.check_output(["sh", "gphoto_dummy.sh"])
        announcer.announce(msg=stdout.decode())


def make_app():
    app = Flask(__name__)

    announcer = EventQueue()
    photo_event = Queue(maxsize=1)
    thread = Thread(target=threaded_task, args=(photo_event, announcer))
    thread.daemon = True
    thread.start()

    @app.route('/')
    def hello_world():
        return render_template('index.html')

    @app.route('/photo', methods=['POST'])
    def photo():
        try:
            photo_event.put(True)
        except queue.Full:
            pass
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

    return app
