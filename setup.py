import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="grpc-client",
    version="0.0.1",
    author="Joseph Yin",
    author_email="josephyin@outlook.com",
    description="grpc client for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/josephyin/grpc_client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)