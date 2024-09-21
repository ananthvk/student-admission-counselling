gtest_dep = dependency('gtest')
e = executable(
    'test_da_algorithm',
    'test_da_algorithm.cpp',
    cpp_args: extra_args,
    dependencies: [gtest_dep, matcher_dep],
)
test('test_da_algorithm', e)