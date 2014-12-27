
from gi.repository import Gtk
from gi.repository import PangoCairo
from gi.repository import Pango
import math

from pprint import pprint


RADIUS = 150
FONT = "Sans Bold 27"
N_WORDS = 10


class Squareset(Gtk.DrawingArea):

    LABEL = 'SquareSet'

    def __init__(self):
        super(Squareset, self).__init__()
        self.set_size_request(300, 300)
        self.connect('draw', self.on_draw)
        self.show_all()

    def on_draw(self, widget, cairo_context):
        # The on_draw is called when the widget is asked to draw itself.
        # Remember that this will be called a lot of times, so it's usually
        # a good idea to write this code as optimized as it can be.

        cairo_context.translate(RADIUS, RADIUS)

        layout = PangoCairo.create_layout(cairo_context)
        layout.set_text("Text", -1)
        desc = Pango.font_description_from_string(FONT)
        layout.set_font_description(desc)

        rangec = range(0, N_WORDS)
        for i in rangec:
            width, height = 0, 0
            angle = (360. * i) / N_WORDS;
            cairo_context.save()
            red   = (1 + math.cos((angle - 60) * math.pi / 180.)) / 2
            cairo_context.set_source_rgb(red, 0, 1.0 - red)
            cairo_context.rotate(angle * math.pi / 180.)
            #/* Inform Pango to re-layout the text with the new transformation */
            PangoCairo.update_layout(cairo_context, layout)
            width, height = layout.get_size()
            cairo_context.move_to(-(float(width) / 1024.) / 2, - RADIUS)
            PangoCairo.show_layout(cairo_context, layout)
            cairo_context.restore()

            pprint(cairo_context)
