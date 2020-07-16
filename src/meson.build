#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU Lesser General Public
#   License as published by the Free Software Foundation; either
#   version 2 of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

sources = files( 'about.c',
	'animation.c',
	'callbacks.c',
	'camera.c',
	'colexp.c',
	'color.c',
	'common.c',
	'dialog.c',
	'dirtree.c',
	'filelist.c',
	'fsv.c',
	'geometry.c',
	'gui.c',
	'ogl.c',
	'scanfs.c',
	'tmaptext.c',
	'viewport.c',
	'window.c',
)

libs_to_link = [
    libmisc,
    # @GTKGL_LIBS@ \
	# @GL_LIBS@ \
	# @GTK_LIBS@
]

# Dirty fix to configure dialog.c so that I don't have to modify the code yet
# it's super dodgy and permanently modifies the source, so...
run_command('../docdir_findreplace.py', 'DOCDIR', '"' + datadir / meson.project_name() + '"', 'dialog.c')

if get_option('buildtype').startswith('debug')
    libs_to_link += debug_lib
    executable(meson.project_name(), sources,
        dependencies: dependencies,
        link_with: libs_to_link,
        # c_args: '"@0@/../data/debug"'.format(meson.current_source_dir()), # This is in the automake, but it doesn't appear to exist & isn't generated when a debug build is configured / compiled.
        include_directories: include_dirs,
        install: true
    )
else
    executable(meson.project_name(), sources,
        dependencies: dependencies,
        link_with: libs_to_link,
        include_directories: include_dirs,
        install: true
    )
endif

# Linker options for math.h/libm? (-lm)

### Meson docs say these aren't required. I can't find them on my system after compiling from source with automake, so...
# EXTRA_DIST = \
# 	xmaps/back.xpm \
# 	xmaps/birdseye_view.xpm \
# 	xmaps/blockdev.xpm \
# 	xmaps/button_cancel.xpm \
# 	xmaps/button_ok.xpm \
# 	xmaps/cd-root.xpm \
# 	xmaps/cd-up.xpm \
# 	xmaps/chardev.xpm \
# 	xmaps/charset.xbm \
# 	xmaps/fifo.xpm \
# 	xmaps/folder.xpm \
# 	xmaps/fsv-icon.xpm \
# 	xmaps/mini-blockdev.xpm \
# 	xmaps/mini-chardev.xpm \
# 	xmaps/mini-fifo.xpm \
# 	xmaps/mini-folder-open.xpm \
# 	xmaps/mini-folder.xpm \
# 	xmaps/mini-regfile.xpm \
# 	xmaps/mini-socket.xpm \
# 	xmaps/mini-symlink.xpm \
# 	xmaps/mini-unknown.xpm \
# 	xmaps/regfile.xpm \
# 	xmaps/socket.xpm \
# 	xmaps/symlink.xpm \
# 	xmaps/unknown.xpm

# INCLUDES = \
# 	-DLOCALEDIR=\"$(localedir)\" \
# 	-DDOCDIR=\"$(docdir)\" \
# 	-I$(top_srcdir)/lib \
# 	$(DEBUG_CFLAGS) \
# 	@GTK_CFLAGS@ \
# 	@GTKGL_CFLAGS@ \
# 	@GL_CFLAGS@
