# Setting up a "writer deck" with a 2" lcd screen

A writer deck is a distraction-free device; unlike a similarly sized phone or tablet, it does just one thing, write! My goal was to create an even smaller and less expensive version of my "pi tablet" (pi zero 2 connected to an elecrow 7" touchscreen, with a bluetooth keyboard).

Parts: Waveshare 2" lcd with dual oled (link below), a pi zero 2 wh (so no soldering but pricier), a "copy holder" clip (artist grade), and an Arteck slim flat bluetooth keyboard (selected because it has a place to clip the holder). Note the clip fits kind of gingerly, you do NOT want to damage the gold cable. Experiment but be careful. Also needed is a 20w (you need about 13w I think) powerbank (go for at least 5000mah) that has microusb or usb-a output (consider your cables, the pi is powered by microusb).

The keyboard is the biggest component; with a folding style model it all fits in a flat 5x7 pen case. With a phone keyboard case you could easily tuck the pi & screen in and have a phone-sized writing device with you at all times. And so on.

This is a learn as you go process, and I was definitely learning as I went. Be prepared to google error messages. 

Having a computer that can ssh in to the pi is more or less vital so you can copy stuff from the internet easily. Please read through the steps before you start, if you're trying it, as you'll need a few cables and such along the way.

## Setting up the Pi

Flash Raspbian lite bookworm, the latest option that uses bookworm (everything I read said trixie would not work) is fine, using Balena Etcher and a 64gb or 128gb card ($15 will cover it). 

Plug a keyboard into the pi (micro usb to whatever your wired keyboard's port is). Plug the temporary screen in; you need an hdmi to mini hdmi cable or adapter (a $10 zero kit should have one).

Set the user to "pi" and give it a sensible and impossible to guess password like "rhubarb" or "bumbleberry" (mmm pie). Put in the SSID (the name of the wifi) and the password.

You need (just off the top of my head) snap if you want helix + marksman. Otherwise nano, micro, or a similar editor will work fine. Also rclone. All that is at the bottom of this document.

Oh, and while you have raspi-config do set the timezone and keyboard to US. Otherwise you might be very confused later when "#" comes out as a literal pound sign.

## Setting up the tiny screen

Bit of a pain in the ass, tbh. But so neat.

I'm using the 2" lcd hat with dual oled screens (https://www.waveshare.com/oled-lcd-hat-a.htm). Wiki here: (https://www.waveshare.com/wiki/OLED/LCD_HAT_(A)). No reason, just thought the little screens would be fun to play with (and they are).

If you lose raspi-config at any point in the process, reinstall it with this:
```
sudo apt install raspi-config
```

If you lose libmm at any point because installing raspi-config uninstalled it:
```
sudo apt-get install --reinstall libraspberrypi0 libraspberrypi-dev libraspberrypi-doc libraspberrypi-bin
```

You will need libmm to be installed each time you reboot.

I followed the instructions step by step. First use raspi-config to turn on spi and i2c. Then go scroll down to the Bookworm specific link (I used the latest bookworm version) & instructions and follow those. At some point you will lose libmm! You can actually check if the screen is black because of this by using ssh, it'll tell you so once you log in.

I did the instructions on a pi with an existing hdmi display, except I did not use raspi-config to turn spi on until after I had pressed the screen onto the pi. Everything worked, but I realized I had forgotten the last two steps using raspi-config and I had also named my 99-fbturbo file ".conf" not ".tilde". 

This actually gives a perfectly usable CLI by commenting out the lines in .bash_profile:
```
    #fbcp &
    #startx  2> /tmp/xorg_errors
```

and to set the resolution to readable add this to /boot/firmware/config.txt:
```
framebuffer_width=220
framebuffer_height=165
```

Note: if you want to go through with the whole install on the wiki page, do it, but be sure to reinstall libmm after using raspi-config but before rebooting. And comment out the two framebuffer lines in config.txt, and also rename your 99-fbturbo file properly. Basically pay attention and don't be me.

Install fbturbo:
```
sudo apt install xserver-xorg-video-fbturbo
```

Changing the hdmi_cvt line doesn't change the resolution, it blanks the screen. You can try the framebuffer lines above again if everything's working as expected.

Now edit the .xinitrc file (from the configs repo) to get rid of all the extra stuff under "openbox". You just need "openbox &" and the line for xterm. Note these are based on using the framebuffer lines above, and you may have to fiddle with the geometry a bit (it's COLS x ROWS).
```bash
openbox &
xterm -fg white -bg black -geometry 34x12
```

Troubleshooting:
```
nano /home/pi/.local/share/xorg/Xorg.0.log
```

Usually ssh'ing in will give you an error message about fbmc if you just need to reinstall libmm.

## general setup

### google drive & sync

Getting a google drive setup as a remote: https://rclone.org/drive/ (it's number 22 as of this writing) You MUST use sudo to set it up or it'll have many errors when you run it later, and the "remote" you set up is per user. You can use the google drive defaults for awhile, if you're willing to wait through occasional rate limiting. Or you can set up your own token and such (way outside my scope to explain, sorry).

To authorize access you will need a computer you can run rclone on that has a browser. The pi zero 2 runs chromium like mud, so consider downloading the windows version or whatever you use as a desktop and running that. The command is given to you in the process and if you're using ssh you can just copy paste it into the windows terminal.

Setting up rclone bisync: https://rclone.org/bisync/ This has the command to copy paste, though you'll need to run it with dudo, and you'll need to fill in your remote name, a colon, and the path of the folder you want to sync, and then also a directory on your pi you want to sync to. Back the folder up on your desktop first. Zip it, stick it in an entirely different place, check the contents/unzip it there to make sure it's valid and working. Then use --dry-run to test before you actually run the command on the pi. 


### helix editor

This is a modal editor. bu it's pretty straightforward. "i" lets you type. if you're in "i" mode esc puts you in "NOR" mode and you can use ":" to type in commands like "theme" or "config-open" or "write" or "quit". Or hit spacebar for a file menu that's great on tiny screens.

Alternatives: micro editor, nano (comes with the pi). I've seen people using Focuswriter too.

```
sudo apt install snapd
snap install helix --classic`
snap install marksman`
```

Pick a theme, add the markdown.strikethrough option as faux comments. Save files as .md to take full advantage of the colors.

Open ~/.configs/helix/config.toml and add:
```
theme = "gruxbox"

[editor]
true-color = true
gutters = []

[editor.soft-wrap]
enable = true

[keys.insert]
"C-s" = ":w"
```

This sets the theme (I typoed gruvbox when making the file so I have my own easy to identify copy to personalize, yay), sets true-color so the theme will work, removes the gutters (spacers, line numbers, just don't have space), enables soft-wrap, and makes ctrl+s save the file.

When helix feels comfortable and you know how to UNDO and REDO properly, you can turn on the autosave by adding a line to the config file for it. Don't do this until you feel solid on how the program works. Sometimes a shortcut will be set up to delete paragraphs or something, and if you don't know how to bring them back it's better to close the whole thing unsaved than autosave.

### playing with the OLEDs

To run one of the provided demo scripts in the background so you can do other stuff:
```
sudo nohup python3 double_ssd1306_128x64.py & <other stuff, or just leave blank>
```

## todo

I've got to think of something fun to do with the oleds! Honestly they're so cute I wish I could use them for writing itself but they're also very small. 
