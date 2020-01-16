import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="entur-py", # Replace with your own username
    version="0.1",
    author="Knut Magnus Aasru",
    author_email="kmaasrud@outlook.com",
    description="Simplified data retrieval from Entur in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kmaasrud/entur-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)