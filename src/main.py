
import time

import tcod

#FONT = 'data/terminal8x8_gs_ro.png'
FONT = 'data/terminal8x12_gs_ro.png'

console = None

def main():
    global console
    tcod.console_set_custom_font(
        FONT,
        tcod.FONT_LAYOUT_ASCII_INROW | tcod.FONT_TYPE_GREYSCALE,
        16, 16
        )
    console = tcod.console_init_root(60, 40, 'Test', False)
    console.print_(0, 0, 'Hello World!')
    tcod.console_flush()
    time.sleep(2)
