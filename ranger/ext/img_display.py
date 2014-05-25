# This software is distributed under the terms of the GNU GPL version 3.

"""Interface for iterm2 inline image drawing
"""

import sys
import ranger.api
import curses
import base64

class ImgDisplayUnsupportedException(Exception):
    pass

class ImageDisplayer(object):
    def __init__(self, fm):
        self.fm = fm

    def initialize(self):
        pass

    def draw(self,path, start_x, start_y, width, height):
        # self.fm.notify("drawing " + str(start_x) + " " + str(start_y) + " " + path)
        # self.fm.open_console("wut")
        self._placeImage(path, start_x, start_y, width, height)

    def clear(self, start_x, start_y, width, height):
        """Clear a part of terminal display."""
        # self.fm.notify("clearing")
        # self.fm.redraw_window()
        self.fm.ui.win.redrawwin()
        self.fm.ui.win.refresh()

    def quit(self):
        pass

    def _placeImage(self,path,x,y,width,height):
        text = self._imageEscape(path,width,height)
        # text = "holy moly"
        curses.putp(curses.tigetstr("sc"))
        move = curses.tparm(curses.tigetstr("cup"), y, x)
        sys.stdout.write(move)
        sys.stdout.write(text)
        curses.putp(curses.tigetstr("rc"))
        sys.stdout.flush()

    def _imageEscape(self, fileName, width, height):
        content = self._readImage(fileName)

        text = "\033]1337;File=name="
        text += base64.b64encode(fileName)
        text += ";size="
        text += str(len(content))
        text += ";inline=1;width="
        text += str(width)
        text += ";height="
        text += str(height)
        text += ":"
        text += base64.b64encode(content)
        text += "\a\n"
        return text

    def _readImage(self, fileName):
        f = open(fileName, "rb")
        try:
            return f.read()
        finally:
            f.close()
