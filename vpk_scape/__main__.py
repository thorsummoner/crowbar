#!/usr/bin/env python3

"""
    VPK (Valve Pak file) gui browser.

    Insired by GCF Scape
"""

import argparse
import vpk_scape.gtk

ARGP = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawTextHelpFormatter,
)
ARGP.add_argument('vpk_file', nargs="?", help='VPK File to browse')


def main(argp=None):
    if argp is None:
        argp = ARGP.parse_args()

    app = vpk_scape.gtk.VpkScapeMainWindow()

    if argp.vpk_file:
        app.vpk_shell = vpk_scape.vpk_shell.VpkShell(
            app,
            argp.vpk_file
        )

    return app.main()

if __name__ == '__main__':
    main()
