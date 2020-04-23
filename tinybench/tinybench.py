import time
import statistics
from scipy import stats

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

