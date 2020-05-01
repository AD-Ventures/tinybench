from tinybench import benchmark, benchmark_env
import unittest

def foo(a, b):
    return a + b

def bar(a):
    pass

def baz():
    pass

def do_nothing(a):
    pass

class TestBenchmarkEnv(unittest.TestCase):
    def test_error(self):
        with self.assertRaises(TypeError):
            benchmark_env(foo)

    def test_none(self):
        env = benchmark_env([])
        self.assertEqual({}, env)

    def test_one(self):
        env = benchmark_env([foo])
        self.assertEqual({'foo':foo}, env)

    def test_two(self):
        env = benchmark_env([foo, bar])
        self.assertEqual({'foo':foo, 'bar':bar}, env)

class TestBenchmark(unittest.TestCase):
    def test_error(self):
        with self.assertRaises(ValueError):
            benchmark(["foo:foo(1,,2)"], 1, 0, globals())

    def test_run_env(self):
        bench = benchmark(["bar(1)"], 2, 2, {'bar':bar})

        self.assertTrue(bench.exec_times)
        self.assertTrue(bench.means)
        self.assertTrue(bench.maxs)
        self.assertTrue(bench.mins)
        self.assertTrue(bench.meds)

        bench = benchmark(["foo:foo(1, 1)", "bar(1)"], 2, 2, {'foo':foo, 'bar':bar})

        self.assertTrue(bench.exec_times)
        self.assertTrue(bench.means)
        self.assertTrue(bench.maxs)
        self.assertTrue(bench.mins)
        self.assertTrue(bench.meds)

    def test_run_globals(self):
        bench = benchmark(["bar(1)"], 2, 2, globals())

        self.assertTrue(bench.exec_times)
        self.assertTrue(bench.means)
        self.assertTrue(bench.maxs)
        self.assertTrue(bench.mins)
        self.assertTrue(bench.meds)

        a = 1
        b = 1
        bench = benchmark(["foo:foo(a, b)"], 1, 0, globals())
        
        self.assertTrue(bench.exec_times)
        self.assertTrue(bench.means)
        self.assertTrue(bench.maxs)
        self.assertTrue(bench.mins)
        self.assertTrue(bench.meds)

        bench = benchmark(["baz:baz()"], 2, 2, globals())

        self.assertTrue(bench.exec_times)
        self.assertTrue(bench.means)
        self.assertTrue(bench.maxs)
        self.assertTrue(bench.mins)
        self.assertTrue(bench.meds)

        do_nothing(a)
        do_nothing(b)

if __name__ == '__main__':
    unittest.main()
