import time
import statistics
import inspect
import re

class tinybench():
    def __init__(self, exec_times):
        self.exec_times = exec_times
        self.means = {}
        self.maxs = {}
        self.mins = {}
        self.meds = {}
        for label, times in exec_times.items():
            self.means[label] = statistics.mean(exec_times[label])
            self.maxs[label] = max(exec_times[label])
            self.mins[label] = min(exec_times[label])
            self.meds[label] = statistics.median(exec_times[label])

    def __str__(self):
        final_str = ""
        for label, times in self.exec_times.items():
            final_str += label + ": mean: " + str(self.means[label]) + " max: " + str(self.maxs[label]) + " min: " + str(self.mins[label]) + " median: " + str(self.meds[label]) + "\n"

        return final_str


# { label : (fname, [args ...]) }
def benchmark_dict(f_dict, ntimes, warmup, process_time = False):
    exec_times = {}
    
    timer = time.time

    if process_time:
        timer = time.process_time

    for label, (fname, args) in f_dict.items():
        for n in range(warmup):
            fname(*args)

        exec_times[label] = []

        for n in range(ntimes):
            prev = timer()
            fname(*args)
            after = timer()
            exec_times[label].append(after - prev)

    return tinybench(exec_times)

def foo(a, b):
    y = 0
    for x in range(100000):
        y += a + b

    return y

def bar(a):
    z = 2
    for x in range(100000):
        z += 1

bench = benchmark_dict({"foo" : (foo, [1, 2]), "bar" : (bar, [8])}, 100, 5, False)
print(bench)


def benchmark_parse(string):
    strip_string  = string.strip()
    label_ind = strip_string.find(":")
    label = string
    if label_ind != -1:
        label = strip_string[0:label_ind]
    func_ind = strip_string.find('(')
    func = strip_string[label_ind + 1:func_ind]
    new_string = strip_string[func_ind + 1:]
    new_string = new_string[:-1]
    args = map(str.strip, new_string.split(","))
    return (label, func, args)

#https://stackoverflow.com/a/14694234
def calling_scope_variable(name):
  frame = inspect.stack()[1][0]
  while name not in frame.f_locals:
    frame = frame.f_back
    if frame is None:
      return None
  return frame.f_locals[name]

# ['label:func(args)', ...]
def benchmark(functions, ntimes, warmup, process_time = False):
    f_dict = {}

    for func in functions:
        label, func, args = benchmark_parse(func)
        processed_args = []
        for arg in args:
            processed_arg = calling_scope_variable(arg)
            if processed_arg is not None:
                processed_args.append(processed_arg)
            else:
                processed_args.append(eval(arg))

        f_dict[label] = (globals()[func], processed_args)

    return benchmark_dict(f_dict, ntimes, warmup, process_time)

def test_it():
    x = 2
    y = 7
    z = 3
    a = benchmark(["foo:foo(x, y)", "bar(z)"], 10, 2)
    print(a)

test_it()
