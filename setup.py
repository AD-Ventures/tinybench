import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tinybench",
    version="1.0.2",
    author="AD Ventures",
    author_email="abir.dahlin.ventures@gmail.com",
    description="A microbenchmark for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AD-Ventures/tinybench",
    packages=setuptools.find_packages(),
    install_requires=['matplotlib'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.3',
)
