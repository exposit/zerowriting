### Eink Screen

So e-ink is a lot more like oled than tft, but it also is *almost* plug and play. You have to install a number of libraries and de-enable the existing SPI screen stuff (basically undo everything from setting up the lcd screen). I'm still early in the process.

Waveshare 2.7" with four buttons, Version 2 supports partial refresh.

# Gotchas (so far)
It's vertical. Which, fair. That's not even really a bad thing, given how text is usually read -- I decided to worry about it later and work with it as is for now.
It's blind. You can run the examples over ssh, unlike the oleds, but even basic troubleshooting of anything requiring on device work (like nohup) is painful. I thought I had my script solid, but...

Also?
Raspbian Bookworm is an absolute tyrant about sudo. Maybe I'm spoiled by dietpi, but imo if it's me, working on my own system, and I fully accept the risks of using root, let me freaking use root without having to sudo everything. Okay, rant over.

Really, the whole blind thing has been the biggest issue; code that works fine on my computer and through ssh sometimes just doesn't when run through xinitrc or similar. So I'm going to have to rethink and simplify. I've got it working about 75% of the way to how I want it to work, but getting it to load the script automatically has proven very hard. And I still need to figure out how I want to handle partial refreshes.
