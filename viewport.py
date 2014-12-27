
from gi.repository import Gtk
from gi.repository import Gdk
from pprint import pprint
from sceene import Sceene
from squareset import Squareset

class Viewport(Gtk.Box):

    XY = Sceene('xy')
    SQUARESET = Squareset()

    CSS = """
        GtkLabel {
            color: %(fg_color)s;
            background: %(bg_color)s;
            border-right-width: 2px; border-bottom-width: 2px;
            border-style: solid; border-color: %(bg_color)s;
            padding-left: 8px; padding-right: 8px;
        }
    """

    overlay = Gtk.Overlay(expand=True)
    scrolled = Gtk.ScrolledWindow(expand=True, can_focus=True)
    label = Gtk.Label()
    menu = Gtk.Menu()
    viewmode = None

    def __init__(self, viewmode):
        super(Viewport, self).__init__()
        self.viewmode = viewmode

        self.init_label()
        self.init_css()

        self.add(self.overlay)
        self.overlay.add(self.scrolled)
        self.scrolled.add(viewmode)
        self.overlay.add_overlay(self.label)

    def init_label(self):
        self.label.set_text(self.viewmode.LABEL)
        self.label.set_name(self.viewmode.LABEL)
        self.label.set_halign(Gtk.Align.START)
        self.label.set_valign(Gtk.Align.START)

    def init_css(self):
        style_context = Gtk.Window().get_style_context()
        color_scheme = {
            'fg_color': '#ffffff',
            'bg_color': '#000000',
        }

        for color in color_scheme.keys():
            try:
                found, rgba = style_context.lookup_color(color)

                if not found:
                    raise KeyError('Color `%s` not found in system theme.' % color)

                color_scheme[color] = rgba

            except KeyError as err:
                pprint(err)

        cssprovider = Gtk.CssProvider()
        css_data = self.CSS % color_scheme
        cssprovider.load_from_data(css_data.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            cssprovider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
