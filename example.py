from gi.repository import Gtk
import signal

from pprint import pprint
import pdb

class Paned(Gtk.Paned):
    """docstring for Paned"""

    loop = False

    def __init__(self, orientation, child1, child2, size, shadow=Gtk.ShadowType.IN):
        super(Paned, self).__init__(orientation=orientation)

        self.child1 = child1
        self.frame1 = Gtk.Frame(shadow_type=shadow)
        self.frame1.set_size_request(*size)
        self.pack1(self.frame1, resize=True, shrink=False)
        self.frame1.add(child1)

        self.child2 = child2
        self.frame2 = Gtk.Frame(shadow_type=shadow)
        self.frame2.set_size_request(*size)
        self.pack2(self.frame2, resize=True, shrink=False)
        self.frame2.add(child2)

    def on_notify(self, _, gparamspec):

        if not gparamspec.name == 'position':
            return

        if self.loop:
            self.loop^=True
            return

        self.loop^=True

        self.linked.props.position = self.props.position

    def bind_resize(self, linked):
        self.connect('notify', self.on_notify)
        self.linked = linked


class GridWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Grid Example")
        self.set_size_request(400, 200)

        link1 = Paned(
            Gtk.Orientation.HORIZONTAL,
            Gtk.Label('viewport'),
            Gtk.Label('TOP'),
            (160, 90)
        )
        link2 = Paned(
            Gtk.Orientation.HORIZONTAL,
            Gtk.Label('LEFT'),
            Gtk.Label('FRONT'),
            (160, 90)
        )
        link1.bind_resize(link2)
        link2.bind_resize(link1)

        self.add(
            Paned(
                Gtk.Orientation.VERTICAL,
                link1, link2,
                (160, 90),
                Gtk.ShadowType.NONE
            )
        )


        # major_pain = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
        # major_pain.set_size_request(320, 180)
        # self.add(major_pain)

        # # minor_pain1 = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        # # minor_pain2 = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        # # minor_pain1.pane_opposite = minor_pain2
        # # minor_pain2.pane_opposite = minor_pain1
        # # major_pain.add1(minor_pain1)
        # # major_pain.add2(minor_pain2)

        # frame_viewport = Gtk.Frame(shadow_type=Gtk.ShadowType.IN)
        # frame_viewport.set_size_request(160, 90)
        # viewport = Gtk.Button('viewport')
        # frame_viewport.add(viewport)

        # frame_xy = Gtk.Frame(shadow_type=Gtk.ShadowType.IN)
        # frame_xy.set_size_request(160, 90)
        # xy = Gtk.Button('TOP')
        # frame_xy.add(xy)

        # # xz = Gtk.Button('FRONT')
        # # yz = Gtk.Button('LEFT')

        # # minor_pain1.add1(viewport)
        # # minor_pain1.add2(xy)
        # # minor_pain2.add1(xz)
        # # minor_pain2.add2(yz)

        # major_pain.pack1(frame_viewport, resize=True, shrink=False)
        # major_pain.pack2(frame_xy, resize=True, shrink=False)

win = GridWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
