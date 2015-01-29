from gi.repository import Gtk
from pprint import pprint

class TableWindow(Gtk.Window):
    viewmode2d = {
        'top': ('x', 'y'),
        'front': ('y', 'z'),
        'side': ('x', 'z'),
    }

    def __init__(self):
        Gtk.Window.__init__(self, title="Table Example")
        self.set_size_request(800, 600)

        table = Gtk.Table(2, 2, True)
        self.add(table)

        button1 = self.viewport3d()
        button2 = self.viewport2d('top')[0]
        button4 = self.viewport2d('front')[0]
        button5 = self.viewport2d('side')[0]
        # pprint((
        #     button5.get_children()[0].get_children()[2].get_hadjustment(),
        #     button5.get_children()[0].get_children()[2].get_vadjustment(),
        # ))

        table.attach(button1, 0, 1, 0, 1)
        table.attach(button2, 1, 2, 0, 1)

        table.attach(button4, 0, 1, 1, 2)
        table.attach(button5, 1, 2, 1, 2)

    def viewport2d(self, direction):
        assert direction in self.viewmode2d, 'Invalid `viewmode2d` "%s"' % direction
        frame = Gtk.Frame()
        frame.set_shadow_type(Gtk.ShadowType.IN)


        overlay = Gtk.Overlay()
        frame.add(overlay)

        label = Gtk.Label("This is a normal label")
        box = Gtk.Box(Gtk.Orientation.HORIZONTAL, 0)
        box.pack_start(label, False, False, 0)
        overlay.add_overlay(box)

        # create the table and pack into the window
        table = Gtk.Table(2, 2, False)
        overlay.add(table)

        # create the layout widget and pack into the table
        layout = Gtk.Layout()
        layout.set_size(1000, 1000)
        table.attach(
            layout,
            0, 1, 0, 1,
            Gtk.AttachOptions.FILL | Gtk.AttachOptions.EXPAND,
            Gtk.AttachOptions.FILL | Gtk.AttachOptions.EXPAND,
            0, 0
        )
        # create the scrollbars and pack into the table
        vScrollbar = Gtk.VScrollbar(None)
        table.attach(
            vScrollbar,
            1, 2, 0, 1,
            Gtk.AttachOptions.FILL | Gtk.AttachOptions.SHRINK,
            Gtk.AttachOptions.FILL | Gtk.AttachOptions.SHRINK,
            0, 0
        )
        hScrollbar = Gtk.HScrollbar(None)
        table.attach(
            hScrollbar,
            0, 1, 1, 2,
            Gtk.AttachOptions.FILL | Gtk.AttachOptions.SHRINK,
            Gtk.AttachOptions.FILL | Gtk.AttachOptions.SHRINK,
            0, 0
        )
        # tell the scrollbars to use the layout widget's adjustments
        vAdjust = layout.get_vadjustment()
        vScrollbar.set_adjustment(vAdjust)
        hAdjust = layout.get_hadjustment()
        hScrollbar.set_adjustment(hAdjust)

        return (frame, hAdjust, vAdjust)
    def viewport3d(self):
        frame = Gtk.Frame()

        return frame

win = TableWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
