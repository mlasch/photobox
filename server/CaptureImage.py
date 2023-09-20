from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

# Kill gphoto2 process that
# starts whenever we connect the
# camera

def killgphoto2Process():
    p = subprocess.Popen (['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    
    # Search for the lline that has the process
    # we want to kill
    
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            #kill the process!
            pid = int(line.split(None,1) [0])
            os.kill(pid, signal.SIGKILL)

shot_date = datetime.now() .strftime ("%Y-%m-%d")
shot_time = datetime.now() .strftime ("%Y-%m-%d %H:%M:%S")
picID = "Pishots"

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", \
                "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

folder_name = shot_date + picID
save_location = "/home/fotobox/Desktop/Fotobox/images/" + folder_name


def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print ("Failed to create the new directory.")
    os.chdir(save_location)


def captureImages(folder):
    gp(triggerCommand)
    sleep(3)
    gp(downloadCommand)
    gp(clearCommand)


def renameFiles(ID):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith(".JPG"):
                os.rename(filename, (shot_time + ID + ".JPG"))
                print("Renamed the JPG")
                return shot_time + ID + ".JPG"
            elif filename.endswith(".CR2"):
                os.rename(filename, (shot_time + ID + ".CR2"))
                print("Renamed the CR2")
                return shot_time + ID + ".CR2"


def take_photo(folder):
    killgphoto2Process()
    gp(clearCommand)
    #createSaveFolder()
    captureImages(folder)
    filename = renameFiles(picID)

    return filename


if __name__ == "__main__":
    take_photo(save_location)