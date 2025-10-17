# Setting up a "writer deck" with a small 2" lcd screen

## Setting up the Pi

Flash Raspbian lite bookworm, the latest option is fine, using Balena Etcher and a 64gb or 128gb card ($15 will cover it). 

You'll be googling a lot, having a computer that can ssh in to the pi is important. 

Plug a keyboard into the pi (requires a microusb to your keyboard). Plug the temporary screen in; you need an hdmi to minihdmi cable but kits will have one).

Set the user to "pi" and give it a sensible and impossible to guess password like "rhubarb" or "bumbleberry" (mmm pie). Put in the SSID (the name of the wifi) and the password.

You need (just off the top of my head) snap if you want helix + marksman. Otherwise nano, micro, or a similar editor will work fine. Also rclone.

## Setting up the tiny screen

Bit of a pain in the ass, tbh. But so neat.

First: I'm using the 2" oled/lcd hat (https://www.waveshare.com/oled-lcd-hat-a.htm). Wiki here: (https://www.waveshare.com/wiki/OLED/LCD_HAT_(A)). With a Raspberry Pi Zero 2 WH.

If you lose raspi-config in the process, reinstall it:
```
sudo apt install raspi-config
```

If you lose libmm because installing raspi-config uninstalled it:
```
sudo apt-get install --reinstall libraspberrypi0 libraspberrypi-dev libraspberrypi-doc libraspberrypi-bin
```

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

Getting a google drive setup as a remote (https://rclone.org/drive/):
``

Setting up rclone bisync (https://rclone.org/bisync/):
``

```
sudo apt install snapd
snap install helix --classic`
snap install marksman`
```

Pick a theme, add the markdown.strikethrough option as faux comments.

Open config.toml and add:
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

To run one of the provided demo scripts in the background so you can do other stuff:
```
sudo nohup python3 double_ssd1306_128x64.py & <other stuff, or just leave blank>
```
