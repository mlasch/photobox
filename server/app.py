import os
import queue
import subprocess
from queue import Queue
from threading import Thread

from flask import Flask, Response, render_template, request

from eventqueue import EventQueue

from CaptureImage import take_photo


def photo_task(photo_event, announcer, logger):
    """Take photo"""
    while True:
        photo_event.get()
        try:
            # stdout = subprocess.check_output(["sh", "gphoto_dummy.sh"])
            # filename = stdout.decode()
            os.chdir("static/images")
            filename = take_photo("")

            announcer.announce(msg=filename)
        except subprocess.CalledProcessError as e:
            logger.warning("Failed to take photo: %s", e)


def print_task(print_event, logger):
    """Send photo to printer"""
    while True:
        filename = print_event.get()
        try:
            stdout = subprocess.check_output(["sh", "gphoto_dummy.sh"])
            print("PRINT ", filename)
        except subprocess.CalledProcessError as e:
            logger.warning("Failed to print photo: %s", e)


def make_app():
    app = Flask(__name__)

    announcer = EventQueue()
    photo_event = Queue(maxsize=1)
    print_event = Queue(maxsize=1)

    photo_thread = Thread(target=photo_task, args=(photo_event, announcer, app.logger), daemon=True)
    photo_thread.start()

    print_thread = Thread(target=print_task, args=(print_event, app.logger), daemon=True)
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
        app.logger.debug("Start listen")

        def stream():
            yield f"data: init\n\n"
            messages = announcer.listen()  # returns a queue.Queue
            while True:
                msg = messages.get()  # blocks until a new message arrives
                yield f"data: {msg}\n\n"

        return Response(stream(), mimetype='text/event-stream')

    return app
