#!/usr/bin/env python

#
# gtkdoc2man.py
#
# Copyright (C) 2012 Christian Hergert <christian@hergert.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
This script will generate a manpage for a given gtk-doc XML file.
It creates manpage links for functions, types, structs, and macros
found within the XML document.

Example usage:
    gtkdoc2man.py --output-directory=man --prefix=GLib xml/arrays.xml

This will generate the given man page for the xml file, prefixed with
GLib- to avoid collisions with other systems. However, functions will
not be prefixed so that they can be used from various editors such as
VIM and Emacs.
"""

import getopt
import os
from pipes import quote
import sys
import tempfile

XSL_URL = 'http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl'

def _sanitizeRefTo(name):
    return name.strip().replace(' ', '_')

def _sanitizeId(name):
    # Work around Gio doing Blah_struct junk.
    if '_struct.' in name:
        name = name.replace('_struct.', '.')
    return name.split(':')[0].replace('-', '_').replace(' ', '_')

def _link(name, refto, output_directory=None, prefix=None, section=3):
    if prefix:
        refto = prefix + ':' + refto
    print '%s => %s (%s)' % (name, refto, section)
    path = os.path.join(output_directory, name + ('.%d' % section))
    f = file(path, 'w')
    f.write('.so man%d/%s\n' % (section, refto))
    f.close()

def _rmtmpdir(tmpdir):
    for f in os.listdir(tmpdir):
        os.unlink(os.path.join(tmpdir, f))
    os.rmdir(tmpdir)

def gtkdoc2man(path, output_directory=None, prefix=None, section=3):
    from lxml.etree import parse, HTMLParser

    if output_directory is None:
        output_directory = os.getcwd()
    if prefix is None:
        prefix = ''

    tmpdir = tempfile.mkdtemp(dir=output_directory)
    refto = None

    try:
        # Generate the man page for the gtkdoc section.
        procargs = ['xsltproc', '-o', tmpdir + '/', '-nonet', XSL_URL, path]
        command = ' '.join([quote(a) for a in procargs])
        os.system(command)

        # Move the file to it's prefixed name.
        for f in os.listdir(tmpdir):
            src = os.path.join(tmpdir, f)
            # Work around Gio doing Blah_struct.3 junk.
            if '_struct.' in f:
                f = f.replace('_struct.', '.')
            dst = os.path.join(output_directory, '%s:%s' % (prefix, f))
            os.rename(src, dst)
            refto = f
    finally:
        _rmtmpdir(tmpdir)

    if not refto:
        print >> sys.stderr, 'Nothing processed in', path
        return

    # Generate the links to the generated manpage.
    tree = parse(path, parser=HTMLParser())
    for child in tree.iter():
        if child.tag == 'refsect2':
            if 'id' in child.attrib and 'role' in child.attrib:
                role = child.attrib['role']
                if role in ('function', 'struct', 'macro', 'typedef'):
                    idstr = _sanitizeId(child.attrib['id'])
                    _link(idstr, refto,
                          output_directory=output_directory,
                          prefix=prefix,
                          section=section)

def usage(stream=sys.stdout):
    print >> stream, """usage: %s [OPTIONS] INPUT...

Options

    -h --help                      Show this help menu.
    -c --check                     Check for runtime dependencies.
    -s --section=3                 The manual section [Default is 3]
    -o --output-directory=DIR      Set the output directory.
    -p --prefix=PREFIX             Prefix output filenames.
""" % sys.argv[0]

if __name__ == '__main__':
    longArgs = ['output-directory=', 'prefix=', 'help', 'check', 'section=']
    shortArgs = 'o:p:hcs:'
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, shortArgs, longArgs)
    except getopt.GetoptError, ex:
        print >> sys.stderr, repr(ex)
        usage(sys.stderr)
        sys.exit(0)

    outdir = None
    prefix = None
    section = 3

    for o,a in opts:
        if o in ('-h', '--help'):
            usage(sys.stdout)
            sys.exit(0)
        elif o in ('-p', '--prefix'):
            prefix = a
        elif o in ('-o', '--output-directory'):
            outdir = a
            if not os.path.exists(outdir):
                os.makedirs(outdir)
        elif o in ('-c', '--check'):
            try:
                from lxml.etree import parse, HTMLParser
            except ImportError:
                print >> sys.stderr, 'lxml.etree is missing.'
                sys.exit(1)
            sys.exit(0)
        elif o in ('-s', '--section'):
            section = int(a)
            assert section >= 0
            assert section < 10

    for path in args:
        if os.path.exists(path):
            gtkdoc2man(path,
                       output_directory=outdir,
                       prefix=prefix,
                       section=section)

    sys.exit(0)
