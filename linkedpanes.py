
from gi.repository import Gtk

class LinkedPanes(Gtk.Bin):
    def __init__(self, tl, tr, bl, br):
        super(LinkedPanes, self).__init__()

        if 'linked-pane':
            link1 = LinkedPane(
                Gtk.Orientation.HORIZONTAL,
                tl, tr,
                (160, 90)
            )
            link2 = LinkedPane(
                Gtk.Orientation.HORIZONTAL,
                bl, br,
                (160, 90)
            )
            link1.bind_resize(link2)
            link2.bind_resize(link1)

        if 'primary-pane':
            self.add(
                Pane(
                    Gtk.Orientation.VERTICAL,
                    link1, link2,
                    (160, 90),
                    Gtk.ShadowType.NONE
                )
            )

class Pane(Gtk.Paned):
    """docstring for Paned"""


    def __init__(self, orientation, child1, child2, size, shadow=Gtk.ShadowType.IN):
        super(Pane, self).__init__(orientation=orientation)

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

class LinkedPane(Pane):

    loop = False

    def __init__(self, *args):
        super(LinkedPane, self).__init__(*args)
        self.connect('button-release-event', self.on_end_resize)

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

    def on_end_resize(self, widget, event):
        """
            Correct real-time positioning mistakes.
            http://stackoverflow.com/a/7892056/1695680
        """
        self.linked.props.position = self.props.position
