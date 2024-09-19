py = import('python').find_installation()
dep_py = py.dependency()
dep_matcher = dependency('matcher')
py.extension_module(
    'pymatcher',
    'pymatcher.pyx',
    dependencies: [dep_py, dep_matcher],
    override_options : ['cython_language=cpp'],
)
