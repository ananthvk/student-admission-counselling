
if meson.get_compiler('cpp').get_id() == 'clang' and get_option('development')
    extra_args = [
        '-Wall',
        '-Wformat=2',
        '-Wshadow',
        '-Wfloat-equal',
        '-Wshift-overflow',
        '-Wextra',
        '-Wconversion',
        '-Wsign-conversion',
        '-Wcast-align',
        '-pedantic',
        '-gdwarf-4',
        '-O',
        '-fsanitize=integer,address,undefined,integer-divide-by-zero,shift,null,return,signed-integer-overflow,float-divide-by-zero,float-cast-overflow,bounds,alignment,vptr,leak',
        '-pedantic',
        '-Wno-sign-compare',
        '-Wno-unused-parameter',
        '-Wno-sign-conversion',
        '-ftrapv',
        '-D_GLIBCXX_DEBUG',
        '-D_GLIBCXX_DEBUG_PEDANTIC',
        '-D_FORTIFY_SOURCE=2',
        '-fstack-protector',
    ]
else
    extra_args = []
endif

executable(
    'main',
    'main.cpp',
    cpp_args: extra_args,
)
if get_option('enable-tests')
    subdir('tests')
endif

