import itertools

from gi.repository import Gtk

from crowbar import web_colors

DEAFULT_ZOOM = 1024
GRID_BOUND = 4096
GRID_HIGHLIGHT = 64
HIDE_GRID_SMALLER_THAN = 8
BSP_SPLIT = 1024

class DictView(Gtk.Bin):

    COLOR_256 = 0xff
    COLOR_PALETTE = {
        'white': (1, 1, 1),
        'black': (0, 0, 0),
        'center-axis': (0, 100/COLOR_256, 100/COLOR_256),
        'bsp-split-axis': (100/COLOR_256, 46/COLOR_256, 1/COLOR_256),
        'grid-axis': (115/COLOR_256, 115/COLOR_256, 115/COLOR_256),
        'highlight-axis': (130/COLOR_256, 130/COLOR_256, 130/COLOR_256),
        'origin-bubble': (0, COLOR_256, COLOR_256),

        'best-laid-plans': (25/COLOR_256, 60/COLOR_256, 74/COLOR_256),
        'hame-fun-with-it': (50/COLOR_256, 101/COLOR_256, 152/COLOR_256),
        'chill-out-dude': (8/COLOR_256, 177/COLOR_256, 235/COLOR_256),
        'rice-paper': (231/COLOR_256, 219/COLOR_256, 194/COLOR_256),
    }

    def __init__(self, viewaxis, geometry, scroll_lock):
        super(DictView, self).__init__()
        self.geometry = geometry
        self.viewaxis = viewaxis

        self.offset = {'x': 0, 'y': 0}
        self.zoom_view = DEAFULT_ZOOM

        if 'init_gtk':
            # Frame
            self._frame = Gtk.Frame()
            self._frame.set_shadow_type(Gtk.ShadowType.IN)
            self.add(self._frame)

            # ScrolledWindow
            self._scrolled = (
                Gtk.ScrolledWindow(
                    hadjustment=scroll_lock[self.viewaxis[0]],
                    vadjustment=scroll_lock[self.viewaxis[1]],
                )
                if scroll_lock['enabled'] else
                Gtk.ScrolledWindow()
            )
            self._scrolled.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)
            self._scrolled.connect('scroll-event', self.on_scroll)
            self._frame.add(self._scrolled)


            self._viewport = Gtk.Viewport()
            self._scrolled.add(self._viewport)

            # DrawingArea
            self._drawingarea = Gtk.DrawingArea()

            if 'scoll_offset':
                self._drawingarea.set_size_request(GRID_BOUND*2, GRID_BOUND*2)
                self._hadjustment = self._scrolled.get_hadjustment()
                self._vadjustment = self._scrolled.get_vadjustment()
                self._scrolled.connect('realize', self._on_scrolled_realized)

            self._drawingarea.connect('draw', self.on_draw)
            self._viewport.add(self._drawingarea)

    def _on_scrolled_realized(self, scolled):
        allocation = scolled.get_allocation()
        self.offset['x'] = GRID_BOUND - allocation.width / 2.0
        self.offset['y'] = GRID_BOUND - allocation.height / 2.0
        self._hadjustment.set_value(self.offset['x'])
        self._vadjustment.set_value(self.offset['y'])


    def on_scroll(self, widget, event):
        # Determine if we should apply scroll acceleration
        # Mouse scoll wheel always emits plus/minus float 1
        # Touch devices _may_ emit plus/minus float 1, but usually not exactly.
        hard_scroll = any([
            # event.delta_x in (1.0, -1.0),
            event.delta_y in (1.0, -1.0),
        ])

        self.zoom_view += event.delta_y
        self._drawingarea.queue_draw()

    def on_draw(self, drawingarea, context):
        allocation = drawingarea.get_allocation()
        center = dict(
            x=allocation.width / 2.0,
            y=allocation.height / 2.0,
        )
        context.set_line_width(1)

        if 'fill':
            self._draw_rectangle(
                context,
                0, 0,
                allocation.width, allocation.height,
                self.COLOR_PALETTE['black']
            )

        if 'grid':
            context.set_source_rgb(*self.COLOR_PALETTE['grid-axis'])
            step = HIDE_GRID_SMALLER_THAN
            for axis in range(0, GRID_BOUND*2, step):
                self._draw_line(context, 0, axis, allocation.width, axis)
                self._draw_line(context, axis, 0, axis, allocation.height)

        if 'highlight':
            context.set_source_rgb(*self.COLOR_PALETTE['highlight-axis'])
            for axis in range(0, GRID_BOUND*2, GRID_HIGHLIGHT):
                self._draw_line(context, 0, axis, allocation.width, axis)
                self._draw_line(context, axis, 0, axis, allocation.height)


        if 'bsp-split-axis':
            context.set_source_rgb(*self.COLOR_PALETTE['bsp-split-axis'])
            # Add 1 to exmapnd range to include final axis.
            for axis in range(0, GRID_BOUND*2+1, BSP_SPLIT):
                self._draw_line(context, 0, axis, allocation.width, axis)
                self._draw_line(context, axis, 0, axis, allocation.height)

        if 'center-axis':
            context.set_source_rgb(*self.COLOR_PALETTE['center-axis'])
            self._draw_line(context, center['x'], 0, center['x'], allocation.height)
            self._draw_line(context, 0, center['y'], allocation.width, center['y'])

        if 'example_geometry':
            colors = itertools.cycle(web_colors.COLORS_INT)
            for geometry in self.geometry:
                color = next(colors)
                context.set_source_rgb(*color)

                points = [
                    [geometry[self.viewaxis[0]][0] + center['x'], geometry[self.viewaxis[1]][0] + center['y']],
                    [geometry[self.viewaxis[0]][1] + center['x'], geometry[self.viewaxis[1]][0] + center['y']],
                    [geometry[self.viewaxis[0]][1] + center['x'], geometry[self.viewaxis[1]][1] + center['y']],
                    [geometry[self.viewaxis[0]][0] + center['x'], geometry[self.viewaxis[1]][1] + center['y']],
                    [geometry[self.viewaxis[0]][0] + center['x'], geometry[self.viewaxis[1]][0] + center['y']],
                ]

                self._draw_lines(context, points)

                for point in points:
                    self._draw_rectangle(
                        context,
                        point[0] - 4,
                        point[1] - 4,
                        8, 8,
                        self.COLOR_PALETTE['black']
                    )
                    self._draw_rectangle(
                        context,
                        point[0] - 3,
                        point[1] - 3,
                        6, 6,
                        self.COLOR_PALETTE['white']
                    )



    @staticmethod
    def _draw_line(context, x1, y1, x2, y2, color=None):
        if color:
            context.set_source_rgb(*color)

        context.move_to(x1 - 0.5, y1 - 0.5)
        context.line_to(x2 - 0.5, y2 - 0.5)
        context.stroke()

    @staticmethod
    def _draw_lines(context, points, color=None):
        if color:
            context.set_source_rgb(*color)

        point = points.pop(0)
        context.move_to(point[0] - 0.5, point[1] - 0.5)
        for point in points:
            context.line_to(point[0] - 0.5, point[1] - 0.5)
        context.stroke()

    @staticmethod
    def _draw_rectangle(context, x1, y1, x2, y2, color=None):
        if color:
            context.set_source_rgb(*color)

        context.rectangle(x1, y1, x2, y2)
        context.fill()
