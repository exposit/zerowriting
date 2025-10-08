#!/bin/sh

# https://bbs.archlinux.org/viewtopic.php?pid=1778781#p1778781
# this is a minimal .xinitrc for my zero writerdeck; you need to install the stuff below
# this just goes in the root folder

# silence annoying accessibility connection bug
export NO_AT_BRIDGE=1

userresources=$HOME/.Xresources
usermodmap=$HOME/.Xmodmap
sysresources=/etc/X11/xinit/.Xresources
sysmodmap=/etc/X11/xinit/.Xmodmap

# merge in defaults and keymaps

if [ -f $sysresources ]; then
    xrdb -merge $sysresources
fi

if [ -f $sysmodmap ]; then
    xmodmap $sysmodmap
fi

if [ -f "$userresources" ]; then
    xrdb -merge "$userresources"
fi

if [ -f "$usermodmap" ]; then
    xmodmap "$usermodmap"
fi

# start some nice programs -- theoretically, I don't actually use this
if [ -d /etc/X11/xinit/xinitrc.d ] ; then
 for f in /etc/X11/xinit/xinitrc.d/?*.sh ; do
  [ -x "$f" ] && . "$f"
 done
 unset f
fi

# sometimes it needs & or && or no & at all
openbox &
# Set the wallpaper
feh --bg-scale ~/Images/74ddb21133dd3a2d7b479bb6833fcd9b.jpg &

# cols and rows, then pixel position, you kind of just have to guess
# this is flipped, I wanted the "anchoring" one on the left, when that closes openbox closes
xterm -fg white -bg black -geometry 50x20+560+0 &
xterm -fg white -bg black -geometry 50x20+20+0

# to just run one of these, comment out the xterm lines and uncomment either of them
#geany
#qpdfview

# this stuff happens after you close the initial window; I don't know how it works
#exec micro --geometry 50x50
