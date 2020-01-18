import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythentur",
    version="0.0.3",
    author="Knut Magnus Aasrud",
    author_email="kmaasrud@outlook.com",
    description="Simplified data retrieval from Entur in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kmaasrud/pythentur",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)