import time
import statistics
from scipy import stats

class tinybench():
    def __init__(self):
        pass


# { label : (fname, [args ...]) }
def benchmark_dict(f_dict, ntimes, warmup):
    exec_time = {}
    f_means = {}
    for label, (fname, args) in f_dict.items():
        for n in range(warmup):
            fname(*args)

        exec_time[label] = []

        for n in range(ntimes):
            prev = time.time()
            fname(*args)
            after = time.time()
            exec_time[label].append(after - prev)

        f_means[label] = statistics.mean(exec_time[label])

    return f_means

def foo(a, b):
    y = 0
    for x in range(100000):
        y += a + b

    return y

def bar(a):
    z = 2
    for x in range(100000):
        z += 1

mean_n = []
mean_w = []
for i in range(50):
    f_means_n = benchmark_dict({"foo" : (foo, [1, 2]), "bar" : (bar, [8])}, 100, 0)
    mean_n.append(f_means_n["foo"])
    f_means_w = benchmark_dict({"foo" : (foo, [1, 2]), "bar" : (bar, [8])}, 100, 15)
    mean_w.append(f_means_w["foo"])
    print(i)

t, prob = stats.ttest_ind(mean_n, mean_w)
print(prob)

