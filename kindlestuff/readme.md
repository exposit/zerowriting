# kindle reflect

This is a crude way to reflect a document you're typing in, by default in the IDE Geany, on a Pi zero, to a kindle paperwhite (or whatever browser), by leveraging the kindle browser and Geany's autosaving feature. Basically a riff on Solarwriter but like, without any of the programming cleverness or security. 

Which is to say, no it won't work on the open internets and no you should not use it to write your magnum opus. Be sensible.

This is entirely cobbled together in an afternoon stuff I'm playing with to avoid Real Writing. May it help someone, even if it's just to say, "damn, I will actually go write instead of procrastinating like you".

Note: I'm assuming you're tinkering on a raspberry pi zero running dietpi, you probably can make it work on other systems.

### Basic steps (with Geany)

1. Install Geany; set the autosave plugin to "enabled" and the duration to 1 second (put it back to 300 when you're not using this, and keep your tmp folder clean).
2. Open a file in the "Scratchpad" directory (might need to make it) called "scratchdoc.md"
3. Edit reflect.py to have your hostname (dietpi shows this when you log in) and preferred document (see prior step) if you don't want to specify it at runtime.
4. In the Geany terminal run `python reflect.py <filename>`, you can leave off the filename if you're using scratchdoc.md
5. Point your desired browser (like on your paperwhite) to the hostname and port.
6. Behold the 1 second lag as you type on your zero-computer and it magically appears on the other screen, at least until you accidentally hit alt-tab or something and have to pull the real screen back up to see wtf you did.

I am aware this is not optimal, or perfect, or even all that useful. Baby steps.

## Thoughts

It's laggy; probably acceptable for brainstorming or sprinting at the park with the e-ink screen. Haven't tested connecting kindle and zero to the same phone hotspot yet, which is kind of important for traveling with it off wifi. The browser refresh is set to 1 second; you can set this higher or lower, but anything lower has noticeable flickering on my paperwhite.

I'm using geany for the autosave and terminal; while I think vnc with display forwarding is an option to control it through a phone, a solution using a terminal CLI like nano or vim that saved on every keystroke would be better.

Or I guess since it's just a scratchpad I could add some sort of basic typer thing to the script. Maybe? Edit: see below.

## Scribble.py

This script opens a scratch document at the command line and types directly into it, saving on each letter. It has NO SAFETY OR SANITY CHECKS. None. Nada. Zero. It won't even quit gracefully.

It should only be used on throwaway documents, like if you're sprinting or brainstorming, and you should copy any words you care about into a proper document (or copy the file somewhere else) as soon as you can.

Repeat: it does not check anything. IT HAS NO SAFETY OR SANITY CHECKS. Obviously don't use it to open anything you care about.

It may skip letters if you type very quickly. You cannot backspace or delete or any of that. Forward only. Joyce it up. 

You run it by typing `python3 scribble.py` after logging in to dietpi and changing to the directory the script is in.

Option "s" will silence the timestamps and work with the file as given, otherwise it'll prepend a timestamp. If you're using reflect, you should use this (as described below).
Option "-f" allows you to specify a filename; if you don't use "s" with it it'll prepend the timestamp as usual, but really, you shouldn't be opening old files with this program anyway.

Ie `python3 scribble.py s -f banana.md` will make a file called "banana.md" or open one in the same directory and start typing in it. Without the "s" it'll be something like "2025blablablah-banana.md". Without either it'll open a timestamped "scribble.md" file. It's stupid simple; avoid using the flags unless you have to. You can edit the script itself to change defaults.

### Basic steps (with reflect)

0. Do step 3 from the Geany steps above, editing reflect.py to match your hostname and port.
1. Change to the script directory, and type (change both filenames if you change one):
  `nohup python3 reflect.py bubblegum3.md & python3 scribble.py s -f bubblegum3.md`
2. Open your desired browser and point to the hostname you specified.
3. Type. When you're done, hit ctrl+c to kill scribble.py and type `killall python3` (or whatever python you called) to end reflect.py.
4. Move any words you care about to a safer place.
