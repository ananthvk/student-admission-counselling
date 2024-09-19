gtest_dep = dependency('gtest')
e = executable(
    'test_da_algorithm',
    'test_da_algorithm.cpp',
    cpp_args: extra_args,
    dependencies: [gtest_dep],
    include_directories: include_dirs
)
test('test_da_algorithm', e)