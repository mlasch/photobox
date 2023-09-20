import queue
import subprocess
from queue import Queue
from threading import Thread

from flask import Flask, Response, render_template, request

from eventqueue import EventQueue


def photo_task(photo_event, announcer):
    """Take photo"""
    while True:
        photo_event.get()
        try:
            stdout = subprocess.check_output(["sh", "gphoto_dummy.sh"])

            announcer.announce(msg=stdout.decode())
        except subprocess.CalledProcessError as e:
            pass


def print_task(print_event):
    """Send photo to printer"""
    while True:
        filename = print_event.get()
        try:
            stdout = subprocess.check_output(["sh", "gphoto_dummy.sh"])
            print("PRINT ", filename)
        except subprocess.CalledProcessError as e:
            pass


def make_app():
    app = Flask(__name__)

    announcer = EventQueue()
    photo_event = Queue(maxsize=1)
    print_event = Queue(maxsize=1)

    photo_thread = Thread(target=photo_task, args=(photo_event, announcer), daemon=True)
    photo_thread.start()

    print_thread = Thread(target=print_task, args=(print_event,), daemon=True)
    print_thread.start()

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

    @app.route('/print', methods=['POST'])
    def _print():
        filename = request.args['filename']
        try:
            print_event.put(f"images/{filename}")
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
