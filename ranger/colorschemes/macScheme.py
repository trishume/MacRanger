# Copyright (C) 2009-2013  Roman Zimbelmann <hut@lepus.uberspace.de>
# This software is distributed under the terms of the GNU GPL version 3.

from ranger.gui.colorscheme import ColorScheme
from ranger.gui.color import *
import stat

class MacScheme(ColorScheme):
    progress_bar_color = blue

    def icon(self, drawn, tagged, tagged_marker):
        mark = u"\ue606"

        if tagged:
            tag_icons = {
                'h':u"\ue600", '*':u"\ue616", 'd':u"\ue60e",
                'g':u"\ue61e", 'c':u"\ue613", 's':u"\ue60f",
                'w':u"\ue627", 'o':u"\ue61b", 'i':u"\ue602",
                'a':u"\ue610",}
            if tagged_marker in tag_icons:
                mark = tag_icons[tagged_marker]
            else:
                mark = tagged_marker
        elif drawn.is_link:
            mark = u"\ue614"
        elif drawn.video:
            mark = u"\ue604"
        elif drawn.image:
            mark = u"\ue601"
        elif drawn.audio:
            mark = u"\ue603"
        elif drawn.container:
            mark = u"\ue60d"
        elif drawn.document:
            mark = u"\ue607"
        elif drawn.is_directory:
            mark = u"\ue609"
        elif drawn.stat and (drawn.stat.st_mode & stat.S_IXUSR):
            mark = u"\ue61c"

        mark += " "
        return mark.encode('utf-8')

    def use(self, context):
        fg, bg, attr = default_colors

        if context.main_column:
            bg = cyan

        if context.reset:
            return default_colors

        elif context.in_browser:
            if context.selected:
                attr = reverse
            else:
                attr = normal
            if context.empty or context.error:
                fg = red
            if context.border:
                fg = default
            # if context.media:
            #     if context.image:
            #         fg = magenta
            #     else:
            #         fg = magenta
            # if context.container:
            #     fg = red
            if context.directory:
                # attr |= bold
                fg = blue
            # elif context.executable and not \
            #         any((context.media, context.container,
            #             context.fifo, context.socket)):
            #     attr |= bold
                # fg = green
            # if context.socket:
            #     fg = magenta
            #     attr |= bold
            # if context.fifo or context.device:
            #     # fg = yellow
            #     if context.device:
            #         attr |= bold
            if context.link:
                fg = magenta
            if context.tag_marker and not context.selected:
                attr = normal
            if context.tagged:
                fg = yellow
            #     attr |= bold
            #     if fg in (red, magenta):
            #         fg = white
            #     else:
            #         fg = red
            if not context.selected and (context.cut or context.copied):
                fg = black
                attr |= bold
            if context.main_column:
                if context.selected:
                    attr |= bold
                if context.marked:
                    attr |= bold
                    fg = red
            if context.badinfo:
                if attr & reverse:
                    bg = magenta
                else:
                    fg = magenta

        elif context.in_titlebar:
            attr |= bold
            if context.hostname:
                fg = context.bad and red or green
            elif context.directory:
                fg = blue
            elif context.tab:
                fg = black
                if context.good:
                    bg = red
                    fg = white
            elif context.link:
                fg = blue

        elif context.in_statusbar:
            if context.permissions:
                if context.good:
                    fg = blue
                elif context.bad:
                    fg = magenta
            if context.marked:
                attr |= bold | reverse
                fg = red
            if context.message:
                if context.bad:
                    attr |= bold
                    fg = red
            if context.loaded:
                bg = self.progress_bar_color
            if context.vcsinfo:
                fg = blue
                attr &= ~bold
            if context.vcscommit:
                fg = red
                attr &= ~bold


        if context.text:
            if context.highlight:
                attr |= reverse

        if context.in_taskview:
            if context.title:
                fg = blue

            if context.selected:
                attr |= reverse

            if context.loaded:
                if context.selected:
                    fg = self.progress_bar_color
                else:
                    bg = self.progress_bar_color


        if context.vcsfile and not context.selected:
            attr &= ~bold
            if context.vcsconflict:
                fg = magenta
            elif context.vcschanged:
                fg = red
            elif context.vcsunknown:
                fg = red
            elif context.vcsstaged:
                fg = green
            elif context.vcssync:
                fg = green
            elif context.vcsignored:
                fg = default

        elif context.vcsremote and not context.selected:
            attr &= ~bold
            if context.vcssync:
                fg = green
            elif context.vcsbehind:
                fg = red
            elif context.vcsahead:
                fg = blue
            elif context.vcsdiverged:
                fg = magenta
            elif context.vcsunknown:
                fg = red

        return fg, bg, attr
