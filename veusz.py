#!/usr/bin/env python

# veusz.py
# Main veusz program file

#    Copyright (C) 2004 Jeremy S. Sanders
#    Email: Jeremy Sanders <jeremy@jeremysanders.net>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##############################################################################

# $Id$

import sys
import qt

import utils
from windows.mainwindow import MainWindow

# if ran as a program
if __name__ == '__main__':

    app = qt.QApplication(sys.argv)

    # process command line arguments
    cmdline = [str(app.argv()[i]) for i in range(1, app.argc())]

    if '--help' in cmdline or len(cmdline) > 1:
        sys.stderr.write('Veusz version %s\n' % utils.version())
        sys.stderr.write('Copyright (C) Jeremy Sanders 2003 '
                         '<jeremy@jeremysanders.net>\n\n')
        sys.stderr.write('Usage: \n veusz saved.vsz\n')
        sys.stderr.write('Optional arguments --help, --version\n')
        sys.exit(0)
    elif '--version' in cmdline:
        sys.stderr.write('Veusz version %s\n' % utils.version())
        sys.stderr.write('Copyright (C) Jeremy Sanders 2003 '
                         '<jeremy@jeremysanders.net>\n')
        sys.exit(0)

    win = MainWindow()
    win.show()
    app.connect(app, qt.SIGNAL("lastWindowClosed()"),
                app, qt.SLOT("quit()"))

    # load in filename given
    if len(cmdline) != 0:
        win.openFile(cmdline[0])

    app.exec_loop()
