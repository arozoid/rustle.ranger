# rstl — deep forest-green colorscheme
# muted pine / moss / woodland palette

from ranger.gui.color import bold, default, default_colors, normal, reverse
from ranger.gui.colorscheme import ColorScheme

# deep forest palette
FG         = 252   # #d0d0d0  main text
HEADER     = 108   # #87af87  soft sage
KEY        = 114   # #87af5f  moss green
MUTED      = 0     # #5f875f  muted pine
GREEN      = 65    # #5f875f  primary forest accent
DIM        = 239   # #4e4e4e
FAINT      = 235   # #262626

RED        = 167   # #d75f5f  muted red
YELLOW     = 143   # #afaf5f  earthy olive
BLUE       = 103   # #8787af  muted slate blue
MAGENTA    = 132   # #af5f87  muted berry
CYAN       = 109   # #87afaf  dusty teal


class Rstl(ColorScheme):
    progress_bar_color = GREEN

    def verify_browser(self, context, fg, bg, attr):
        if context.selected:
            # subtle moss selection
            bg = MUTED
            fg = KEY
            attr |= bold
        else:
            attr = normal

        if context.empty or context.error:
            bg = RED
            fg = FAINT

        if context.border:
            fg = GREEN

        if context.document:
            attr |= normal
            fg = FG

        if context.media:
            if context.image:
                fg = YELLOW
            elif context.video:
                fg = MAGENTA
            elif context.audio:
                fg = CYAN
            else:
                fg = FG

        if context.container:
            attr |= bold
            fg = YELLOW

        if context.directory:
            attr |= bold
            fg = HEADER

        elif context.executable and not any(
            (context.media, context.container, context.fifo, context.socket)
        ):
            attr |= bold
            fg = GREEN

        if context.socket:
            fg = MAGENTA
            attr |= bold

        if context.fifo or context.device:
            fg = YELLOW
            if context.device:
                attr |= bold

        if context.link:
            fg = CYAN if context.good else RED

        if context.tag_marker and not context.selected:
            attr |= bold
            if fg in (RED, MAGENTA):
                fg = KEY
            else:
                fg = RED

        if not context.selected and (context.cut or context.copied):
            fg = DIM
            attr |= bold

        if context.main_column:
            if context.selected:
                attr |= bold
            if context.marked:
                attr |= bold
                fg = YELLOW

        if context.badinfo:
            if attr & reverse:
                bg = MAGENTA
            else:
                fg = MAGENTA

        if context.inactive_pane:
            fg = DIM

        return fg, bg, attr

    def verify_titlebar(self, context, fg, bg, attr):
        bg = HEADER
        fg = FAINT
        attr |= bold

        if context.hostname:
            fg = RED if context.bad else FAINT
        elif context.directory:
            fg = FAINT
        elif context.tab:
            if context.good:
                bg = GREEN
                fg = FAINT
        elif context.link:
            fg = CYAN

        return fg, bg, attr

    def verify_statusbar(self, context, fg, bg, attr):
        if context.permissions:
            if context.good:
                fg = GREEN
            elif context.bad:
                bg = RED
                fg = FG

        if context.marked:
            attr |= bold | reverse
            fg = YELLOW

        if context.frozen:
            attr |= bold | reverse
            fg = CYAN

        if context.message:
            if context.bad:
                attr |= bold
                fg = RED

        if context.loaded:
            bg = self.progress_bar_color

        if context.vcsinfo:
            fg = BLUE
            attr &= ~bold

        if context.vcscommit:
            fg = YELLOW
            attr &= ~bold

        if context.vcsdate:
            fg = CYAN
            attr &= ~bold

        return fg, bg, attr

    def verify_taskview(self, context, fg, bg, attr):
        if context.title:
            fg = BLUE

        if context.selected:
            attr |= reverse

        if context.loaded:
            if context.selected:
                fg = self.progress_bar_color
            else:
                bg = self.progress_bar_color

        return fg, bg, attr

    def verify_vcsfile(self, context, fg, bg, attr):
        attr &= ~bold

        if context.vcsconflict:
            fg = MAGENTA
        elif context.vcschanged:
            fg = RED
        elif context.vcsunknown:
            fg = RED
        elif context.vcsstaged:
            fg = GREEN
        elif context.vcssync:
            fg = GREEN
        elif context.vcsignored:
            fg = default

        return fg, bg, attr

    def verify_vcsremote(self, context, fg, bg, attr):
        attr &= ~bold

        if context.vcssync or context.vcsnone:
            fg = GREEN
        elif context.vcsbehind:
            fg = RED
        elif context.vcsahead:
            fg = CYAN
        elif context.vcsdiverged:
            fg = MAGENTA
        elif context.vcsunknown:
            fg = RED

        return fg, bg, attr

    def use(self, context):
        fg, bg, attr = default_colors

        if context.reset:
            return default_colors

        elif context.in_browser:
            fg, bg, attr = self.verify_browser(context, fg, bg, attr)

        elif context.in_titlebar:
            fg, bg, attr = self.verify_titlebar(context, fg, bg, attr)

        elif context.in_statusbar:
            fg, bg, attr = self.verify_statusbar(context, fg, bg, attr)

        if context.text and context.highlight:
            attr |= reverse

        if context.in_taskview:
            fg, bg, attr = self.verify_taskview(context, fg, bg, attr)

        if context.vcsfile and not context.selected:
            fg, bg, attr = self.verify_vcsfile(context, fg, bg, attr)
        elif context.vcsremote and not context.selected:
            fg, bg, attr = self.verify_vcsremote(context, fg, bg, attr)

        return fg, bg, attr
