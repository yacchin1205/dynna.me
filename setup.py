import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

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
    package_dir={"": ""},
    packages=setuptools.find_packages(where="dynname_proxy"),
    python_requires=">=3.6",
)
