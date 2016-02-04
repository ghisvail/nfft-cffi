# Copyright (c) 2016, Imperial College London
# Copyright (c) 2016, Ghislain Antony Vaillant
# All rights reserved.
#
# Distributed under the terms of the new BSD license.
# See the accompanying LICENSE file or read the terms at
# https://opensource.org/licenses/BSD-3-Clause.

from setuptools import find_packages, setup


def get_install_requires():
    from distutils.version import StrictVersion
    from sys import version_info
    install_requires = ['cffi>=1.0.0', 'numpy']
    py_version = StrictVersion('.'.join(str(n) for n in version_info[:3]))
    if py_version < StrictVersion('3.4'):
        install_requires.append('enum34')


setup(
    name = 'nfft-cffi',
    version = '0.1',
    description = 'Python interface to the NFFT library',
    url = 'https://github.com/ghisvail/nfft-cffi',
    author = 'Ghislain Antony Vaillant',
    author_email = 'ghisvail@gmail.com',
    license = 'BSD',
    classifiers = [
        'Development Status :: 3 - Alpha'
        'Intended Audience :: Science/Research'
        'License :: OSI Approved :: BSD License'
        'Programming Language :: Python'
        'Topic :: Software Development'
    ],
    keywords = 'gridding nfft nufft nusfft',
    packages=find_packages(exclude=['builders', 'docs', 'tests']),
    setup_requires=['cffi>=1.0.0', 'pkgconfig', 'nose>=1.0'],
    install_requires=get_install_requires(),
    ext_package='nfft',
    cffi_modules=['builders/build_bindings.py:ffi'],
)