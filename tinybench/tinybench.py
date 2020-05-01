import time
import statistics
import inspect
import matplotlib.pyplot as plt

class tinybench():
    """
    Benchmark with associated statistics and graphics.

    ...

    Methods
    -------
    __str__()
        String representation of the benchmark data
        
    plot()
        Creats and shows a violin plot for the benchmark data

    """
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

        self.units = "us"
        for t in self.maxs.values():
            if t >= 0.01:
                self.units = "s"
                break

            if t >= 0.00001:
                self.units = "ms"

    def __str__(self):
        final_str = ""
        for label, times in self.exec_times.items():
            final_str += label + ": mean: " + str(self.means[label]) +\
                " max: " + str(self.maxs[label]) + " min: " +\
                str(self.mins[label]) + " median: " + str(self.meds[label]) +\
                "\n"

        return final_str

    def plot(self):
        if self.units == "us":
            units = "microseconds"
            data = [[x * 1000000 for x in y] for y in list(self.exec_times.values())]
        elif self.units == "ms":
            units = "milliseconds"
            data = [[x * 1000 for x in y] for y in list(self.exec_times.values())]
        else:
            units = "seconds"
            data = list(self.exec_times.values())

        labels = list(self.exec_times.keys())
        fig, ax = plt.subplots()

        ax.violinplot(data, vert=False)
        ax.set_yticks(range(1, len(labels) + 1))
        ax.set_yticklabels(labels)
        ax.set_xlabel("Time in {}".format(units))
        ax.set_title("Violin Plot of Runtimes")
        plt.tight_layout()  # so labels are not cutoff
        plt.show()


# { label : (fname, [args ...]) }
def benchmark_dict(f_dict, ntimes, warmup, process_time=False):
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


def benchmark_parse(string):
    strip_string = string.strip()
    label_ind = strip_string.find(":")
    label = string
    if label_ind != -1:
        label = strip_string[0:label_ind]
    func_ind = strip_string.find('(')
    func = strip_string[label_ind + 1:func_ind]
    new_string = strip_string[func_ind + 1:]
    new_string = new_string[:-1]
    args = list(map(str.strip, new_string.split(",")))
    if args == ['']:
        args = []
    return (label, func, args)


# https://stackoverflow.com/a/14694234
def calling_scope_variable(name):
    frame = inspect.stack()[1][0]
    while name not in frame.f_locals:
        frame = frame.f_back
        if frame is None:
            return None
    return frame.f_locals[name]


# ['label:func(args)', ...]
def benchmark(functs, ntimes, warmup, g, process_time=False):
    """
    Benchmarks functions supplied in the first argument.

    This function provides support for timing and comparing runtimes
    of various supplied functions.

    Paramters
    ---------
    functs : list of str
        List of strings with strings follown the format of 'label:func(args)'
    ntimes : int
        the number of times to run each function
    warmup : int
        the number of inital runs to throw out before calculating runtimes
    pocess_time : bool, default False
        whether to return process time or elapsed (real) runtimes

    Returns
    -------
    benchmark
        an object of class benchmark

    Examples
    --------
    >>> def foo(a, b): return a + b
    >>> b = benchmark(["foo:foo(1, 2)"], 10, 3, globals())
    >>> print(b)
    foo: mean: 9.5367431640625e-08 max: 9.5367431640625e-07 min: 0.0 median: 0.0
    """
    f_dict = {}

    for func in functs:
        label, func, args = benchmark_parse(func)
        processed_args = []
        for arg in args:
            if arg == '':
                raise ValueError("Invalid empty argument")
            processed_arg = calling_scope_variable(arg)
            if processed_arg is not None:
                processed_args.append(processed_arg)
            else:
                processed_args.append(eval(arg))

        f_dict[label] = (g[func], processed_args)

    return benchmark_dict(f_dict, ntimes, warmup, process_time)

def benchmark_env(functions):
    """
    Returns a map from function names to function symbols.

    Use this in conjunction with benchmark if a fine-grained list
    of functions is necessary.

    Paramters
    ---------
    functions : list of function
        The list of function symbols that will be used as a benhcmarking environment

    Returns
    -------
    env
        a map from function names to function symbols

    Examples
    --------
    >>> def foo(): pass
    >>> env = benchmark_env([foo])
    >>> print(env)
    {'foo': <function foo at 0x104bf49e0>}
    """
    if type(functions) != list:
        raise TypeError("Invalid list argument type 'functions'")
    env = {}
    for f in functions:
        env[f.__name__] = f
    return env
