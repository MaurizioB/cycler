cycler
======

A window switcher made in pygtk for DE that do not provide a system one (like
Fluxbox). I was not satisfied with bbkeys and needed something more powerful,
so I decided to try to make one by myself.

Still at early development stage, alt key release is a big problem, since the
gtk's keybinder module does not allow to detect a key release (or at least I
do not know how).


Running
-------

Just launch it :)
Alt-Tab switches to the next window, Alt-Shift-Tab to the previous.
The windows are not activated until the Alt key is released, unless you keep
the focus on a specific window button for a second: this will activate the
selected window.
You can also use the mouse to click on a window button to activate it.
Press Esc button at any moment to close the switcher without switching to the
selected window.


Known issues
------------

Some special windows might create unexpected focus behaviour, expecially full
screen ones, like mplayer.