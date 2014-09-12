#!/usr/bin/env python
# -*- coding: utf-8 -*

import gtk, pango
import keybinder
import wmctrl, wnck
from commands import getoutput
from time import sleep

pos = (1764, 180)


class Cycler():
    def __init__(self):
        #self.windowList = wmctrl.Window.list()
        self.screen = wnck.screen_get_default()
        self.windowList = self.screen.get_windows()
        self.cycler = gtk.Window(type=gtk.WINDOW_POPUP)
        self.cycler.set_title('cycler')
        self.cycler.set_role('cycler')
        #self.cycler.set_skip_taskbar_hint(True)
        #self.cycler.set_skip_pager_hint(True)
        self.cycler.set_decorated(False)
        self.cycler.set_keep_above(True)
        self.cycler.set_resizable(False)
        self.cycler.set_accept_focus(True)

        #self.cycler.set_default_size(640, -1)

        self.hidden = gtk.Window()
        self.hidden.connect('key-release-event', self._release)
        self.hidden.set_decorated(False)
        self.hidden.set_skip_taskbar_hint(True)
        self.hidden.set_skip_pager_hint(True)
        self.hidden.set_default_size(0, 0)
        #self.hidden.connect('focus-out-event', self._hide)
        #self.hidden.iconify()
        
        #self.cycler.connect('key-press-event', self._press)
        self.cycler.connect('show', self._shown)
        self.cycler.connect('hide', self._hidden)
        #self.cycler.connect('focus-out-event', self._hide)
        #self.cycler.connect('window-state-event', self._alert)
        #self.cycler.connect('button-release-event', self._raise)

        self.wlist = gtk.VBox()
        self.wlist.show()
        self.cycler.add(self.wlist)

        #self.default_style = self.wlist.get_style().copy()
        #self.default_style.bg[gtk.STATE_PRELIGHT] = self.default_style.bg[gtk.STATE_NORMAL]


        self.old = False
        self.focusing = 0
        self.selected = gtk.gdk.Color('#bcc')

        #self.cycler.set_position(gtk.WIN_POS_NONE)
        self.cycler.move(*pos)
        #self.cycler.set_position(gtk.WIN_POS_CENTER)
        self._binder()

    def _binder(self):
        keybinder.bind('<Alt>Tab', self._altTab, 1)
        keybinder.bind('<Alt>ISO_Left_Tab', self._altTab, -1)
        #keybinder.bind('Alt_L', self._alert)
        #keybinder.bind('<Release>s', self._alert)

    def _alert(self):
        #print dir(event)
        print 'bagr'
        return
        print event.get_state
        print event.new_window_state

    def _hide(self, window, event):
        print 'hide'
        self.cycler.hide()
        self.hidden.hide()

    def _hidden(self, window):
        self.hidden.hide()
        return
        #print 'hidden'
        try:
            keybinder.bind('<Alt>Tab', self._altTab)
        except:
            pass

    def _altTab(self, direction):
        self.focusing += direction

        if not self.cycler.get_property('visible'):
            self.cycler.show()
            self.hidden.show()
            self.hidden.move(-1, -1)

        if self.focusing >= len(self.ordered):
            self.focusing = 0
        if self.focusing < 0:
            self.focusing = len(self.ordered)-1
        self._focus()


    def _shown(self, window):
        #self.cycler.present()
        #self.cycler.move(1464, 180)
        rootwinlist = getoutput('xwininfo -root -tree').split('\n')
        #keybinder.unbind('<Alt>Tab')
        #current = wmctrl.Window.get_active()
        current = self.screen.get_active_window()
        ws = self.screen.get_active_workspace()
        winlist = [w for w in self.screen.get_windows() if w.get_workspace() == ws and w.get_name() != 'cycler']
        #winnames = [w.id[3:] for w in winlist]
        self.ordered = []
        #self.focusing = 1
        for w in rootwinlist:
            if 'has no name' in w:
                continue
            self.ordered.extend([o for o in winlist if hex(o.get_xid())[2:-1] in w])
        self._update()

    def _update(self):
        if self.ordered != self.old:
            for o in self.wlist.children():
                o.destroy()
            for w in self.ordered:
                box = gtk.HBox(False, 0)
                wimage = gtk.Image()
                wimage.set_from_pixbuf(w.get_icon())
                wlabel = gtk.Label()
                #wlabel.set_property('max-width-chars', 80)
                wlabel.set_ellipsize(pango.ELLIPSIZE_END)
                wlabel.set_size_request(500, -1)
                wlabel.set_alignment(xalign=0.0, yalign=0.5)
                wclass = w.get_class_group().get_res_class()
                wtitle = w.get_name()
                if wclass != '':
                    #wname = '<span size="24000"><b>%s</b> %s</span>' % (wclass, wtitle)
                    wname = '<span size="24000"><b>%s</b> %s</span>' % (wclass, wtitle)
                else:
                    wname = '<span size="24000"><b>%s</b></span>' % (wtitle)
                wlabel.set_markup(wname)
                box.pack_start(wimage, False, False, 2)
                box.pack_start(wlabel, False, False, 8)
                
                wimage.show()
                wlabel.show()
                wbutton = gtk.Button()

                style = wbutton.get_style().copy()
                style.bg[gtk.STATE_PRELIGHT] = style.bg[gtk.STATE_NORMAL]
                #wbutton.set_style(style)

                wbutton.modify_bg(gtk.STATE_ACTIVE, self.selected)
                wbutton.connect_after('enter-notify-event', self._normalize)
                #wbutton.connect('button-release-event', self._raise)
                wbutton.add(box)
                box.show()
                self.wlist.add(wbutton)
                wbutton.show()
            self.old = self.ordered
        self.cycler.set_position(gtk.WIN_POS_CENTER)


    def _normalize(self, widget, event):
        widget.set_state(gtk.STATE_NORMAL)
        return False

    def _focus(self):
        for i, w in enumerate(self.ordered):
            #print dir(self.wlist.children()[0])
            if i == self.focusing:
                #f = '*'
                self.wlist.children()[i].set_state(gtk.STATE_ACTIVE)
            else:
                #f = ' '
                self.wlist.children()[i].set_state(gtk.STATE_NORMAL)
            #print '%s\tfocus: %i\tname:%s' % (f, i, w.get_name())

    def _raise(self, widget, event):
        print widget


    def _press(self, window, event):
        print 'press'
        return
        key = gtk.gdk.keyval_name(event.keyval)
        #print key
        if key == 'Tab':
            self.focusing += 1
            if self.focusing >= len(self.ordered):
                self.focusing = 0
            self._focus()
        if key == 'ISO_Left_Tab':
            self.focusing -= 1
            if self.focusing < 0:
                self.focusing = len(self.ordered)-1
            self._focus()

    def _release(self, window, event):
        key = gtk.gdk.keyval_name(event.keyval)
        #print key
        if key == 'Alt_L' or key == 'Meta_L':
            self.cycler.hide()
            if self.ordered:
                self.ordered[self.focusing].activate(event.time)
        elif key == 'Escape':
            self.cycler.hide()
        else:
            return False
        #self.cycler.move(*pos)
        self.cycler.set_position(gtk.WIN_POS_CENTER)


cycler = Cycler()
#keybinder.bind('<Alt>Tab', cycler.cycler.show)


gtk.main()