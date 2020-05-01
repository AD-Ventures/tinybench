from tinybench import benchmark

def foo(a, b):
    return a + b

print(globals())
a = benchmark(["foo:foo(1, 2)"], 10, 3)
#print(a)
#a.plot()
