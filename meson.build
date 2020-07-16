project('fsv', 'c', version: '0.9.0', meson_version: '>=0.55', default_options: ['prefix=/usr'])

# Define a few paths that we'll use later
datadir = get_option('datadir')

cc = meson.get_compiler('c')

cdata = configuration_data()

as_version  = meson.project_version()
ver_arr = as_version.split('.')
as_major_version = ver_arr[0]
as_minor_version = ver_arr[1]
as_micro_version = ver_arr[2]

# Set some config info
cdata.set_quoted('PACKAGE_VERSION', as_version)
cdata.set_quoted('PACKAGE', meson.project_name())
cdata.set_quoted('PACKAGE_NAME', 'File System Visualiser')

### Since we're using autotools configure, set debug configs if building a debug build.
if get_option('buildtype').startswith('debug')
  cdata.set('DEBUG', 1)
  cdata.set('G_ENABLE_DEBUG', 1)
else
  cdata.set('G_DISABLE_ASSERT', 1)
  cdata.set('G_DISABLE_CHECKS', 1)
  cdata.set('GTK_NO_CHECK_CASTS', 1)
endif

if get_option('nls')
  cdata.set('ENABLE_NLS', 1)
endif

dependencies = [dependency('glib-2.0', version: '>=2.38'),
    dependency('gtk+-2.0'),
    dependency('gtkgl-2.0'),
    dependency('GL') # This just ensures that *some* kind of GL support is available.
]

# Set _GNU_SOURCE so that we work properly when POSIX functions are not avaiolable on a non-linux system.
if ['linux', 'cygwin', 'gnu', 'freebsd', 'gnu/kfreebsd'].contains(host_machine.system())
  cdata.set('_GNU_SOURCE', 1)
endif

### Do most of the config.h configuration here; generated using ac_converter.py.
check_headers = [
  ['GTK_DISABLE_COMPAT_H', 'disable/compat.h'],
  ['HAVE_ALLOCA_H', 'alloca.h'],
  ['HAVE_DIRENT_H', 'dirent.h'],
  ['HAVE_INTTYPES_H', 'inttypes.h'],
  ['HAVE_MEMORY_H', 'memory.h'],
  ['HAVE_NDIR_H', 'ndir.h'],
  ['HAVE_STDINT_H', 'stdint.h'],
  ['HAVE_STDLIB_H', 'stdlib.h'],
  ['HAVE_STRINGS_H', 'strings.h'],
  ['HAVE_STRING_H', 'string.h'],
  ['HAVE_SYS_DIR_H', 'sys/dir.h'],
  ['HAVE_SYS_NDIR_H', 'sys/ndir.h'],
  ['HAVE_SYS_STAT_H', 'sys/stat.h'],
  ['HAVE_SYS_TIME_H', 'sys/time.h'],
  ['HAVE_SYS_TYPES_H', 'sys/types.h'],
  ['HAVE_UNISTD_H', 'unistd.h'],
]

foreach h : check_headers
  if cc.has_header(h.get(1))
    cdata.set(h.get(0), 1)
  endif
endforeach

check_functions = [
  ['HAVE_CATGETS', 'catgets', '#include<nl_types.h>'],
  ['HAVE_STPCPY', 'stpcpy', '#include<string.h>'],
  ['HAVE_ALLOCA', 'alloca', '#include<alloca.h>'],
  ['HAVE_CFLOCALECOPYPREFERREDLANGUAGES','CFLocaleCopyPreferredLanguages','#include<CoreFoundation/CFLocale.h>'],
  ['HAVE_CFPREFERENCESCOPYAPPVALUE','CFPreferencesCopyAppValue','#include<CoreFoundation/CoreFoundation.h>'],
  ['HAVE_DCGETTEXT', 'dcgettext', '#include<libintl.h>'],
  ['HAVE_FNMATCH', 'fnmatch', '#include<fnmatch.h>'],
  ['HAVE_GETCWD', 'getcwd', '#include<unistd.h>'],
  ['HAVE_GETTIMEOFDAY', 'gettimeofday', '#include<sys/time.h>'],
  ['HAVE_MKTIME', 'mktime', '#include<unistd.h>'],
  ['HAVE_SCANDIR', 'scandir', '#include<dirent.h>'],
  ['HAVE_STRCSPN', 'strcspn', '#include<string.h>'],
  ['HAVE_STRDUP', 'strdup', '#include<string.h>'],
  ['HAVE_STRFTIME', 'strftime', '#include<time.h>'],
  ['HAVE_STRCSPN', 'strspn', '#include<string.h>'],
  ['HAVE_STRTOD', 'strtod', '#include<stdlib.h>'],
  ['HAVE_STRTOUL', 'strtoul', '#include<stdlib.h>'],
  ['HAVE_STRUCT_STAT_ST_BLOCKS', 'stat', '#include<sys/stat.h>'],
]

# CoreFoundation Stuff: # Best guess from OSX doco
# STRUCT_STAT_ST_BLOCKS: # Define to 1 if `st_blocks' is a member of `struct stat'. This isn't quite right, but it should be fine.
# check token ['HAVE_LC_MESSAGES'] for I18n/L10n; is it looking for the ENV variable?

foreach f : check_functions
  if cc.has_function(f.get(1), prefix : f.get(2))
    cdata.set(f.get(0), 1)
  endif
endforeach

file = find_program('file', required : true) # is it false?
if file.found()
  filepath = file.full_path() # Should just pass 'file' below, but that can't be added to a string.
  cdata.set('HAVE_FILE_COMMAND', 1)
  cdata.set_quoted('FILE_COMMAND', filepath + ' %s') # Pass the location of the file binary; %s because it was in autotools...
endif

# Do LIBM check here for now. Kinda hacky, I'm tired.
if cc.find_library('m', required: true).found() # Is it actually required?
  cdata.set('HAVE_LIBM', 1)
endif

if find_program('xgettext', required : false).found()
  cdata.set('HAVE_GETTEXT', 1)
  found_gettext = true
endif

### Begin OpenGL Config
GL_LDOPTS = ''

# Set GL Prefix & find GL libs / headers
# Autotools checks for the main function within the lib, but that seems way overengineered.
gl_prefix = get_option('GL-prefix')
if gl_prefix != ''
  cdata.set_quoted('GL_CFLAGS','-I'+ gl_prefix / 'include')
  GL_LDOPTS='-L'+ gl_prefix / 'lib'
  header_glu = cc.has_header(gl_prefix / 'GL/glu.h', required: true) # OpenGL Utility Library required.
  lib_mesagl = cc.find_library(gl_prefix / 'MesaGL')
  lib_gl = cc.find_library(gl_prefix / 'GL')
else
  header_glu = cc.has_header('GL/glu.h', required: true) # OpenGL Utility Library required.
  lib_mesagl = cc.find_library('MesaGL', required: false)
  lib_gl = cc.find_library('GL', required: false)
endif

# Dependency check should have ensured *some* openGL support.
# Respect user selection, else prefer OpenGL over Mesa as per existing config.

if get_option('with-lib-GL')
	cdata.set_quoted('GL_LIBS', GL_LDOPTS + ' -lGL -lGLU')
elif get_option('with-lib-MesaGL')
  cdata.set_quoted('GL_LIBS', GL_LDOPTS + ' -lMesaGL -lMesaGLU')
elif lib_gl.found()
	cdata.set_quoted('GL_LIBS', GL_LDOPTS + ' -lGL -lGLU')
else
	cdata.set_quoted('GL_LIBS', GL_LDOPTS + ' -lMesaGL -lMesaGLU')
endif

# Not including a check for no GL here as that *shouldn't* be possible.
### End OpenGL Configuration

docdir = datadir / meson.project_name()


configure_file(input : 'config.h.meson',
  output : 'config.h',
  configuration : cdata
)

# define
include_dirs = [ ]
include_dirs += include_directories('.')

# xgettext is optional (on Windows for instance)
if get_option('nls') and found_gettext == true # We should provide an error if xgettext not found; but this will do for now
  subdir('po')
endif

subdir('data')
subdir('intl')
subdir('lib')
subdir('debug')
subdir('src')

# Keeping this as a reminder to work out setting strictness later on.
# AUTOMAKE_OPTIONS = foreign
# EXTRA_DIST = NOTES TODO fsv.spec fsv.spec.in fsv.wmconfig # Meson docs say no need to include these.
