# Tinybench

Tinybench is a lightweight package to time and compare various functions.  This package was inspired by the R package [microbenchmark](https://cran.r-project.org/web/packages/microbenchmark/index.html)

## Installation

```bash
pip install tinybench
```

## Usage

```python
import tinybench

#create two functions example functions to test
def foo(a):
	test = []
	for i in range(a):
		test.append(i)
	return test

def bar(a, b):
	return a + b

#example input variable
c = 10000


b = tinybench.benchmark(['Display Name for Foo Test:foo(c)', 'bar(10, 15)'])
print(b)
b.plot()
```

## Support

For any help or questions, please email ....

## License

[MIT](https://chosealicense.com/licenses/mit)