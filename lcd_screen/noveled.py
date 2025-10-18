# noveled.py
# for use with the 2" LCD and dual oled screens; you could repurpose it for whatever but it's not pretty or educationcal code, it just works well enough.
#
# when run with nohup, it watches the directory it is run from and if a file changes, the word count from it and its parent folder are updated to the oled screens
# it also has buttons for sprints; one button is unused
#
# note most of the features are naive/blind/interrupt the others, and it's entirely possible to confuse it
# existing files are NEVER opened for writing

# it really only deals with markdown files
# it's real basic, lots of copy paste and very few functions, using the waveshare demos and SO searches

# do our imports
import sys
import time
import os
import time
import threading
from PIL import ImageFont
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

# button imports
from gpiozero import Button

# majorly underutilizing this just to get the system font, you could probably do more
from matplotlib import font_manager
#Find the path for a specific font
fontfile = font_manager.findfont('DM Mono')

# watch the Writing folder, and if a file changes, that's our "current file" for this process.
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# left
serial_32 = i2c(port=1, address=0x3C)
device_32 = ssd1306(serial_32, width=128, height=64)

# right
serial_64 = i2c(port=1, address=0x3D)
device_64 = ssd1306(serial_64, width=128, height=64)

#execution_count = 0  		# Initialize the execution count counter
#max_execution_count = 60	# Specify the maximum number of executions so we can clear the screen occasionally
last_file = ""              # this is used to store the last saved file for sprinting

# Define the button object and specify the BCM pin number
key1 = Button(4)
key2 = Button(17)
key3 = Button(23)
key4 = Button(24)

# 15 minute timer
def key1_pressed():
    #print("Press KEY1(BCM4) SPRINT!")
    # catch the last saved file as our "starting point"
    global last_file
    if os.path.isfile(last_file):
        # get word count from last file and then save it for after the timer
        with open(last_file, 'r') as f:
            # get the word count here; this is super basic and has no checking for comments or anything
            startingwordcount = len(f.read().split())
        run_timer(15*60)
        # now repeat
        with open(last_file, 'r') as f:
            endingwordcount = len(f.read().split())
        wcdiff = endingwordcount - startingwordcount
        draw_text(f"Wrote: {wcdiff}", device_64.width, device_64.height, 36, device_64)
    else:
        draw_text(f"Save once first.", device_32.width, device_32.height, 12, device_32)
        return

# 25 minute timer
def key2_pressed():
    #print("Press KEY2(BCM17)")
    # also catch the last saved file as our "starting point"
    global last_file
    if os.path.isfile(last_file):
        # get word count from last file and then save it for after the timer
        with open(last_file, 'r') as f:
            # get the word count here; this is super basic and has no checking for comments or anything
            startingwordcount = len(f.read().split())
        run_timer(25*60)
        # now repeat word count
        with open(last_file, 'r') as f:
            endingwordcount = len(f.read().split())
        wcdiff = endingwordcount - startingwordcount
        draw_text(f"Wrote: {wcdiff}", device_64.width, device_64.height, 36, device_64)
    else:
        draw_text(f"Save once first.", device_32.width, device_32.height, 12, device_32)
        return

def key3_pressed():
    print("Press KEY3(BCM23)")
    # this doesn't do anything yet except test stuff

# five minute break
def key4_pressed():
    #print("Press KEY4(BCM24)")
    draw_text(f"BREAK!", device_64.width, device_64.height, 36, device_64)
    run_timer(5*60)
    draw_text(f"BACK TO\nWORK!", device_64.width, device_64.height, 24, device_64)

# Bind key press event
key1.when_pressed = key1_pressed
key2.when_pressed = key2_pressed
key3.when_pressed = key3_pressed
key4.when_pressed = key4_pressed

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        #print(f'event type: {event.event_type}  path : {event.src_path}')
        if os.path.isfile(event.src_path):
            if event.src_path.split(".")[-1] in ['md', 'txt']:
                global last_file
                last_file = event.src_path
                changed_file_diff(event.src_path)

def draw_text(text, width, height, fontsize, device):
    font = ImageFont.truetype(fontfile, fontsize)
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        # Calculate the width of the text using textlength() instead of textsize()
        w = font.getlength(text)
        # Calculate the height of the text by subtracting the font descent from the font ascent
        ascent, descent = font.getmetrics()
        h = ascent - descent
        # Calculate the position of the text
        x = (width - w) // 2
        y = (height - h) // 2
        # Draw the text using the new width and height values
        draw.text((10, 1), text, font=font, fill="white")

def get_total_counts(folder):

    filenames = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    filenames = [f for f in filenames if not f.startswith(".")]
    filenames = [f for f in filenames if f.endswith(".md")]
    filenames.sort()

    totalwordcount = 0
    totalgoal = 0
    for fname in filenames:
        with open(os.path.join(folder,fname), 'r') as f:
            # get the word count here; this is super basic and has no checking for comments or anything
            wordcount = len(f.read().split())
            # get the word-goal from the doc, if not set it to 3001
            goal = f.read().split("word-goal: ")[-1].split("\n")[0]
            try:
                goal = int(goal)
            except:
                goal = 3001

            totalwordcount += wordcount
            totalgoal += goal

    return(totalwordcount, totalgoal)

# do the thing; return the string/list/data
def changed_file_diff(changed_file):
    # do the current file
    with open(changed_file, 'r', encoding='latin1') as f:
        wordcount = len(f.read().split())
        # get the word-goal from the doc, if not set it to 3001
        goal = f.read().split("word-goal: ")[-1].split("\n")[0]
        try:
            goal = int(goal)
        except:
            goal = 3001

    prefix = wordcount
    suffix = goal
    fill = "*"
    percent = int(int(wordcount) / int(goal) * 100)
    filledLength = 12 * (wordcount / float(goal))
    bar = fill * int(filledLength) + "-" * (12 - int(filledLength))
    text = f'{prefix}/{suffix} {percent}%\n[{bar}]'

    if int(percent) > 100:
        text = f"{wordcount}/{goal}!\n{percent}%!\nGOAL MET!"

    # display info
    filename = changed_file.split(os.sep)[-1][0:15]
    text = f"{filename}\n{text}"
    draw_text(text, device_64.width, device_64.height, 12, device_64)

    # now do the full directory, if we're not in the root writing folder
    if not os.path.dirname(changed_file) == ".":
        text = ""
        twc, tgo = get_total_counts(os.path.dirname(changed_file))
        bencha = 50000
        benchb = 100000
        benchmark = bencha
        bstr = "50k"
        if twc > bencha:
            benchmark = benchb
            bstr = "100K"
        fill = "*"
        percent = int(int(twc) / int(benchmark) * 100)
        filledLength = 10 * (twc / float(bencha))
        bar = fill * int(filledLength) + " " * (10 - int(filledLength))
        text = f'{twc}/{bstr}  {percent}%'
        text = text + f'\n[{bar}]'

        percent = int(int(twc) / int(benchb) * 100)
        adj_twc = twc - 50000
        adj_goal = 50000
        if adj_twc < 0:
            adj_twc = 0
        filledLength = 10 * (adj_twc / float(adj_goal))
        bar = fill * int(filledLength) + " " * (10 - int(filledLength))
        text = text + f'\n[{bar}]'

        # now add the human readable directory
        posslist = [f for f in os.path.dirname(changed_file).split(os.sep) if not f == "rough draft"]
        posslist = [f for f in posslist if not f == "."]
        displayfolder = str(posslist[-1])[0:15]

        # and put it all together neatly
        text = f"{displayfolder}\n{text}"
        if int(percent) > 100:
            text = f"{displayfolder}\n{twc}/{benchmark}\n{percent}%! THE END!"
        draw_text(text, device_32.width, device_32.height, 12, device_32)

def run_timer(seconds):
    for remaining in range(seconds, 0, -1):
        minutes = 0
        seconds = remaining
        if remaining > 60:
            minutes = int(seconds/60)
            seconds = int(seconds%60)
        else:
            seconds = remaining
        text = "%02d:%02d" % (minutes,seconds)
        draw_text(text, device_32.width, device_32.height, 36, device_32)
        time.sleep(1)

    draw_text("DONE!", device_32.width, device_32.height, 36, device_32)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5) # let's set this higher, we don't need to be checking every second
            #execution_count += 1
            # going to use this to clear the screens every so often for safety; it resets every time a file changes so you should never see it while working
            #if execution_count >= max_execution_count:
            #    draw_text("safety break", device_32.width, device_32.height, 12, device_32)
            #    draw_text("safety break", device_64.width, device_64.height, 12, device_64)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()
