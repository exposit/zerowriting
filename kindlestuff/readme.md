# kindle reflect

This is a crude way to reflect a document you're typing in Geany (on a Pi zero) to a kindle paperwhite, leveraging the kindle browser and Geany's autosaving feature. Basically a riff on Solarwriter but like, without any of the programming cleverness or security. Which is to say, no it won't work on the open internets and no you should not use it to write your magnum opus. Be sensible.

1. Install Geany; set the autosave plugin to "enabled" and the duration 1 second (put it back to 300 when you're not using this).
2. Load up a file called "scratchdoc.md"
3. Edit reflect.py to have your hostname and preferred document (see prior step)
4. In the Geany terminal run `python reflect.py`
5. Point your desired browser to the hostname and port.
6. Behold the 1 second lag as you type on your zero-computer and it magically appears on the other screen, at least until you accidentally hit alt-tab or something and have to pull the real screen back up to see wtf you did.

I am aware this is not optimal, or perfect, or even all that useful. Baby steps.

## Thoughts
It's laggy; probably acceptable for brainstorming or sprinting at the park with the e-ink screen. Haven't tested connecting kindle and zero to the same phone hotspot yet. 

I'm using geany for the autosave and terminal; while I think vnc with display forwarding is an option, a solution using nano or vim that saved on every keystroke would be better.

Or I guess since it's just a scratchpad I could add some sort of basic typer thing to the script. Maybe.
