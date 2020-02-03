from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="sniffbot",
    version="1.0.",
    author="Jon Connolly",
    author_email="joncon@uw.edu",
    description="HTTPS API for eworm utitlites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pnsn/sniffbot",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
