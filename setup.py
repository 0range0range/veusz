#!/usr/bin/env python3

#    Copyright (C) 2008 Jeremy S. Sanders
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
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
##############################################################################

"""
Veusz distutils setup script
see the file INSTALL for details on how to install Veusz
"""

import sys
import glob
import os.path
import numpy

import setuptools
from setuptools import setup, Extension
from setuptools.command.install import install as orig_install
from setuptools.command.install_data import install_data
import pyqtdistutils

if sys.version_info[0] < 3:
    raise RuntimeError('Veusz only supports Python 3')

# get version
with open('VERSION') as verf:
    version = verf.read().strip()

class install(orig_install):
    user_options = orig_install.user_options + [
        # tell veusz where to install its data files
        (
            'veusz-resource-dir=', None,
            'override veusz resource directory location'
        ),
        (
            'disable-install-examples', None,
            'do not install examples files'
        ),
    ]
    boolean_options = orig_install.boolean_options + [
        'disable-install-examples',
    ]

    def initialize_options(self):
        orig_install.initialize_options(self)
        self.veusz_resource_dir = None
        self.disable_install_examples = False

# Pete Shinner's distutils data file fix... from distutils-sig
#  data installer with improved intelligence over distutils
#  data files are copied into the project directory instead
#  of willy-nilly
class smart_install_data(install_data):
    def run(self):
        install_cmd = self.get_finalized_command('install')
        if install_cmd.veusz_resource_dir:
            # override location with veusz-resource-dir option
            self.install_dir = install_cmd.veusz_resource_dir
        else:
            # change self.install_dir to the library dir + veusz by default
            self.install_dir = os.path.join(install_cmd.install_lib, 'veusz')

        # disable examples install if requested
        if install_cmd.disable_install_examples:
            self.data_files = [
                f for f in self.data_files if f[0][-8:] != 'examples'
            ]

        return install_data.run(self)

descr = '''Veusz is a 2D and 3D scientific plotting package, designed to
create publication-ready PDF and SVG output. It features GUI,
command-line, and scripting interfaces. Graphs are constructed from
"widgets", allowing complex layouts to be designed. Veusz supports
plotting functions, data with errors, keys, labels, stacked plots,
multiple plots, and fitting data.'''

def findData(dirname, extns):
    """Return tuple for directory name and list of file extensions for data."""
    files = []
    for extn in extns:
        files += glob.glob(os.path.join(dirname, '*.'+extn))
    files.sort()
    return (dirname, files)

if 'bdist_wheel' in sys.argv:
    # data files can't be installed inside wheels, so don't bother pip
    raise RuntimeError("This setup.py does not support wheels") 

setup(
    name = 'veusz',
    version = version,
    description = 'A scientific plotting package',
    long_description = descr,
    author = 'Jeremy Sanders',
    author_email = 'jeremy@jeremysanders.net',
    url = 'https://veusz.github.io/',
    license = 'GPLv2+',
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: '
        'GNU General Public License v2 or later (GPLv2+)',
        'Topic :: Scientific/Engineering :: Visualization'
    ],
    python_requires='>=3.3',

    data_files = [
        ('', ['VERSION', 'AUTHORS', 'ChangeLog', 'COPYING']),
        findData('ui', ('ui',)),
        findData('icons', ('png', 'svg')),
        findData('examples', ('vsz', 'py', 'csv', 'dat')),
    ],
    packages = [
        'veusz',
        'veusz.dataimport',
        'veusz.datasets',
        'veusz.dialogs',
        'veusz.document',
        'veusz.helpers',
        'veusz.plugins',
        'veusz.qtwidgets',
        'veusz.setting',
        'veusz.utils',
        'veusz.widgets',
        'veusz.windows',
    ],

    ext_modules = [
        # threed support
        Extension(
            'veusz.helpers.threed',
            [
                'veusz/helpers/src/threed/camera.cpp',
                'veusz/helpers/src/threed/mmaths.cpp',
                'veusz/helpers/src/threed/objects.cpp',
                'veusz/helpers/src/threed/scene.cpp',
                'veusz/helpers/src/threed/fragment.cpp',
                'veusz/helpers/src/threed/numpy_helpers.cpp',
                'veusz/helpers/src/threed/clipcontainer.cpp',
                'veusz/helpers/src/threed/bsp.cpp',
                'veusz/helpers/src/threed/twod.cpp',
                'veusz/helpers/src/threed/threed.sip'
            ],
            language="c++",
            include_dirs=[
                'veusz/helpers/src/threed', numpy.get_include()
            ],
        ),

        # mathml widget
        Extension(
            'veusz.helpers.qtmml',
            [
                'veusz/helpers/src/qtmml/qtmmlwidget.cpp',
                'veusz/helpers/src/qtmml/qtmml.sip'
            ],
            language="c++",
            include_dirs=['veusz/helpers/src/qtmml'],
        ),

        # device to record paint commands
        Extension(
            'veusz.helpers.recordpaint',
            [
                'veusz/helpers/src/recordpaint/recordpaintdevice.cpp',
                'veusz/helpers/src/recordpaint/recordpaintengine.cpp',
                'veusz/helpers/src/recordpaint/recordpaint.sip'
            ],
            language="c++",
            include_dirs=['veusz/helpers/src/recordpaint'],
        ),

        # contour plotting library
        Extension(
            'veusz.helpers._nc_cntr',
            [
                'veusz/helpers/src/nc_cntr/_nc_cntr.c'
            ],
            include_dirs=[numpy.get_include()]
        ),

        # qt helper module
        Extension(
            'veusz.helpers.qtloops',
            [
                'veusz/helpers/src/qtloops/qtloops.cpp',
                'veusz/helpers/src/qtloops/qtloops_helpers.cpp',
                'veusz/helpers/src/qtloops/polygonclip.cpp',
                'veusz/helpers/src/qtloops/polylineclip.cpp',
                'veusz/helpers/src/qtloops/beziers.cpp',
                'veusz/helpers/src/qtloops/beziers_qtwrap.cpp',
                'veusz/helpers/src/qtloops/numpyfuncs.cpp',
                'veusz/helpers/src/qtloops/qtloops.sip'],
            language="c++",
            include_dirs=[
                'veusz/helpers/src/qtloops',
                numpy.get_include()
            ],
        ),
    ],

    # new command options
    cmdclass = {
        'build_ext': pyqtdistutils.build_ext,
        'install_data': smart_install_data,
        'install': install
    },

    # requires these modules to install
    install_requires = [
        'numpy', 'PyQt5'
    ],

    # optional requirements
    extras_require = {
        "optional": [
            'astropy', 'pyemf', 'sampy', 'iminuit', 'h5py'
        ]
    },

    # GUI entry points
    entry_points = {
        'gui_scripts' : [
            'veusz = veusz.veusz_main:run',
        ]
    },
)
