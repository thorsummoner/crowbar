#!/usr/bin/env python

import window
import os

class ExampleWindow(window.Window):
    """
        Gui application interface.
    """

    GLADE_FILE = os.path.splitext(__file__)[0] + '.glade'

    def __init__(self):
        super(ExampleWindow, self).__init__()


    class Handler(window.Window.BaseHandler):
        """
            Main Window Event Handler
        """


if __name__ == '__main__':
    exit(ExampleWindow().main())
