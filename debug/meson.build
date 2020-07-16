if get_option('buildtype').startswith('debug')
    sources = files('debug.c')
    debug_lib = static_library('debug', sources, dependencies: dependencies, include_directories: include_dirs, install: false)
    include_dirs += include_directories('.')
endif
