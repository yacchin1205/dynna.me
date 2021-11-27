import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def _requires_from_file(filename):
    return open(filename).read().splitlines()

setuptools.setup(
    name="dynname-proxy",
    version="0.1.0",
    author="Satoshi Yazawa",
    author_email="yazawa@yzwlab.net",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yacchin1205/dynname-proxy",
    project_urls={
        "Bug Tracker": "https://github.com/yacchin1205/dynname-proxy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=_requires_from_file('requirements.txt'),
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
