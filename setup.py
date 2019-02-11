import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iec104",
    version="0.0.1",
    author="Ivan Alexandrov",
    author_email="i1729van@gmail.com",
    description="iec60870-104-5 server based on libiec60870 (MZ-Automation)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/i1729van/py60870server",
    packages=setuptools.find_packages(),
    dependency_links=['git@gitlab.com:peavy/peavy-client.git'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
