import time
import subprocess
from plyer import notification

def play_sound():
    subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"])

def main():
    while True:
        notification.notify(
            title='Hey there!',
            message='Get up, move, drink water, rest your eyes',
            app_icon='glass.ico',
            timeout=5
        )
        play_sound()
        time.sleep(60*45)

if __name__ == "__main__":
    main()
