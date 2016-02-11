=========
nfft-cffi
=========

Compute non-uniform fast Fourier transforms in Python.


Installation
============

Requirements
------------

The following dependencies are required to build, run and test the package:

  - setuptools
  - pkgconfig
  - numpy
  - cffi
  - nose

An installation of the NFFT library (version 3.3 or later) is also required. It should be discoverable with a call to pkg-config::

  $ pkg-config --libs nfft3

Local or non-system installation locations are supported using PKG_CONFIG_PATH::

  $ export PKG_CONFIG_PATH=$HOME/local/lib/pkgconfig
  $ pkg-config --libs nfft3

Using pip
---------

The recommended way to install the package is via pip::

  $ pip install nfft-cffi

Using setup.py 
--------------

This method is suitable for environments where pip is not available, or for testing modifications to the package::

  $ python setup.py install


Contributing
============

Guidelines
----------

The development team welcomes feedback, code and enhancement proposals to the package from the community. Please consider opening an issue or submitting patches for inclusion to the code base via pull-request. For code contributions, please provide appropriate test cases for each new features and verify that the complete test suite runs successfully.

Running the tests
-----------------

If the bindings were modified, then one should first rebuild the CFFI module with::

  $ python setup.py build_ext --inplace

Before running the test suite with a call to::

  $ python setup.py nosetests


License
=======

The **nfft-cffi** source code is released under the terms of the `new BSD license <https://opensource.org/licenses/BSD-3-Clause>`_. The copyright information can be checked out in the accompanying `LICENSE <LICENSE>`_ file.

A separate installation of the NFFT library is required. The source code can be downloaded from the official `homepage <https://www-user.tu-chemnitz.de/~potts/nfft/download.php>`_ and installed following the instructions available in the corresponding README file. The NFFT library is licensed under the `GPL version 2 or later <http://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html>`_. 