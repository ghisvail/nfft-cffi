# Copyright (c) 2016, Imperial College London
# Copyright (c) 2016, Ghislain Antony Vaillant
# All rights reserved.
#
# Distributed under the terms of the new BSD license.
# See the accompanying LICENSE file or read the terms at
# https://opensource.org/licenses/BSD-3-Clause.

from setuptools import find_packages, setup

setup(
    name="nfft-cffi",
    version="0.1.dev1",
    packages=find_packages(exclude=["builders", "docs", "tests"]),
    setup_requires=["cffi>=1.0.0", "pkgconfig"],
    install_requires=["cffi>=1.0.0", "numpy"],
    ext_package="nfft",
    cffi_modules=["builders/build_bindings.py:ffi"],
)
