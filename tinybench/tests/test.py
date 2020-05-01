from tinybench import benchmark, benchmark_env

def foo(a, b):
    return a + b

a = benchmark(["foo:foo(1, 2)"], 10, 3, globals())
print(a)
a = benchmark(["foo:foo(1, 2)"], 10, 3, {'foo':foo})
print(a)
a = benchmark(["foo:foo(1, 2)"], 10, 3, benchmark_env([foo]))
print(a)
a.plot()
