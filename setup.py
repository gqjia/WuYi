#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WuYi",
    version="0.0.1",
    author="Jia Guoqing",
    author_email="jiaguoqing12138@gmail.com",
    description="A small NLP tool package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Moriarty12138/WuYi",
    project_urls={
        "Bug Tracker": "https://github.com/Moriarty12138/WuYi/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "wuyi"},
    packages=setuptools.find_packages(where="wuyi"),
    python_requires=">=3.6",
)