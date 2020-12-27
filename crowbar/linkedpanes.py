
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

    _lp_user_activated = False

    def __init__(self, *args):
        super(LinkedPane, self).__init__(*args)
        self.connect('notify::position', self.on_position)
        self.connect('button-press-event', self.on_button_press)
        self.connect('button-release-event', self.on_button_release)

    def on_position(self, _, gparamspec):
        if self._lp_user_activated:
            self.linked.child_on_position(self.props.position)

    def child_on_position(self, position):
        self.set_position(position)

    def on_button_press(self, *_):
        self._lp_user_activated = True

    def on_button_release(self, *_):
        """
            Correct real-time positioning mistakes.
            http://stackoverflow.com/a/7892056/1695680
        """
        self._lp_user_activated = False
        self.linked.set_position(self.props.position)

    def bind_resize(self, linked):
        self.linked = linked
