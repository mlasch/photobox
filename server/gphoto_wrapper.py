import signal
import os
import subprocess
from pathlib import Path
from time import sleep
from datetime import datetime


class Camera:
    _GPHOTO_PROCESS = "gvfsd-gphoto2"
    _TEMP_FOLDER = "temp_photos"
    _CLEAR_ARGS = ["--folder", "/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]
    _TRIGGER_ARGS = ["--capture-image-and-download"]
    _DOWNLOAD_ARGS = ["--get-all-files"]

    def __init__(self, target_location):
        self.target_location = target_location

    def _kill_gphoto(self):
        """Kill gphoto2 process that starts whenever we connect the camera"""
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate()

        # Search for the line that has the process
        # we want to kill
        for line in out.splitlines():
            if self._GPHOTO_PROCESS in line.decode():
                # kill the process!
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

    def _run_command(self, args, folder=None):
        """Run gphoto2 command"""
        try:
            """
            New file is in location /store_00020001/DCIM/100CANON/IMG_5405.JPG on the camera
            Saving file as IMG_5405.JPG
            Deleting file /store_00020001/DCIM/100CANON/IMG_5405.JPG on the camera
            """
            #subprocess.run(["bash", "/home/marc/repos/photobox/server/gphoto_dummy.sh"] + args, cwd=folder, stdout=subprocess.DEVNULL)
            subprocess.run(["gphoto2"] + args, cwd=folder, stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            raise e

    def take_photo(self, folder):
        """Take photo and copy the result into target directory"""
        # Kill residual gphoto process
        self._kill_gphoto()
        # Remove all photos on camera
        #self._run_command(self._CLEAR_ARGS)
        # Take photo
        self._run_command(self._TRIGGER_ARGS, folder=folder)
        # Wait some time for the photo to be taken
        #sleep(5)
        # Copy photo into folder
        #self._run_command(self._DOWNLOAD_ARGS, folder=folder)
        # Cleanup camera
        #self._run_command(self._CLEAR_ARGS)

        for filename in os.listdir(folder):
            print(filename)
            if filename.endswith(".JPG") or filename.endswith(".jpg"):
                shot_time = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
                new_filename = "photo_" + shot_time + ".jpg"
                os.rename(Path(folder)/Path(filename), Path(self.target_location)/Path(new_filename))

                return new_filename


if __name__ == "__main__":
    camera = Camera("static/images")
    camera.take_photo("temp_photos")
