# This software is distributed under the terms of the GNU GPL version 3.

"""Interface for iterm2 inline image drawing
"""

import sys
import ranger.api
import curses
import base64
import subprocess

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
        text = self._escapeSequence(path,width,height)
        # text = "holy moly"
        curses.putp(curses.tigetstr("sc"))
        move = curses.tparm(curses.tigetstr("cup"), y, x)
        sys.stdout.write(move)
        sys.stdout.write(text)
        curses.putp(curses.tigetstr("rc"))
        sys.stdout.flush()

    def _escapeSequence(self, fileName, width, height):
        if self._is_image_file(fileName):
            return self._imageEscape(fileName, width, height)
        if self.fm.settings.using_macranger_app:
            return self._qlMacRangerEscape(fileName, width, height)
        return self._qlEscape(fileName, width, height)

    def _imageEscape(self, fileName, width, height):
        content = self._readImage(fileName)
        b64 = base64.b64encode(content)
        return self._iTermEscape(fileName, b64, len(content), width, height)

    def _qlEscape(self, fileName, width, height):
        content = self._quicklook_data(fileName, width, height)
        size = len(base64.b64decode(content))
        return self._iTermEscape(fileName, content, size, width, height)

    def _iTermEscape(self, fileName, content, length, width, height):
        text = "\033]1337;File=name="
        text += base64.b64encode(fileName)
        text += ";size="
        text += str(length)
        text += ";inline=1;width="
        text += str(width)
        text += ";height="
        text += str(height)
        text += ":"
        text += content
        text += "\a\n"
        return text

    def _qlMacRangerEscape(self, fileName, width, height):
        text = "\033]1337;File=name="
        text += base64.b64encode(fileName)
        text += ";size=1;inline=1;width="
        text += str(width)
        text += ";height="
        text += str(height)
        text += ":q\a\n"
        return text

    def _readImage(self, fileName):
        f = open(fileName, "rb")
        try:
            return f.read()
        finally:
            f.close()

    def _is_image_file(self, path):
        p = path.lower()
        for ext in ['.png', '.gif', '.jpg', '.psd', '.tiff']:
            if p.endswith(ext):
                return True
        return False

    def _quicklook_data(self, fileName, width, height):
        qltool = self.fm.relpath('data/QLTool.app/Contents/MacOS/QLTool')
        command = [qltool, 'di', fileName, str(width*10), str(height*10)]
        # self.fm.ui.destroy()
        # sys.stderr.write(str(command) + "\n")
        # sys.exit(1)
        data = subprocess.check_output(command)
        return data
