#SCRIBBLE
# if you omit "s" it will automatically prepend a timestamp
# if you omit -f for the filename it'll use "scribble.md" and append

# usage: after logging in, change to the script directory and type
#    nohup python3 reflect.py bubblegum3.md & python3 scribble.py s -f bubblegum3.md
# where 'bubblegum3.md' is the name of the file you want to use
# ctrl+c kills this file, killall python3 (or whatever python you called) ends the reflect script

# https://stackoverflow.com/questions/3523174/raw-input-without-pressing-enter
def getch():
    import sys, termios

    fd = sys.stdin.fileno()
    orig = termios.tcgetattr(fd)

    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ICANON
    new[6][termios.VMIN] = 1
    new[6][termios.VTIME] = 0

    try:
        termios.tcsetattr(fd, termios.TCSAFLUSH, new)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, orig)

# no editing, no clearing, no backspacing, no saving manually, nothing, just new doc if specified
import time
import argparse

timestr = time.strftime("%Y%m%d-%H%M%S-")

parser = argparse.ArgumentParser()
parser.add_argument('-f', nargs='?') # specify a filename
parser.add_argument('s', nargs='?') # use no timestamps
args = parser.parse_args()

if args.s:
    timestr = ""

if args.f:
    scratchdoc = f"{timestr}{args.f}"
else:
    scratchdoc = f"{timestr}scribble.md"

print(f"Loaded: {scratchdoc}")

x = 1 # toggle for the while, to get out, ctrl+c

while not x == 0:
    with open(scratchdoc, "a") as f:
        print('', end='', flush=False)
        c = getch()
        if c == b'^[':
            print('QUIT!')
            exit()
        f.write(c)
