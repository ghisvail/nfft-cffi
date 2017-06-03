"""Common utility functions."""
# Copyright (c) 2016-2017, Imperial College London
# Copyright (c) 2016-2017, Ghislain Antony Vaillant
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the BSD license. See the accompanying LICENSE file
# or read the terms at https://opensource.org/licenses/BSD-3-Clause.

__all__ = ('rand_unit_complex', 'rand_unit_shifted')


def rand_unit_complex(shape, ftype='double'):
    """Return random complex values in the [0, 1) interval.

    Parameters
    ----------
    shape : int or sequence of ints
        Output shape. For instance, if the shape is ``(m, n)``, then ``m * n``
        samples are drawn.
    ftype : str or dtype, optional
        Output float type. Choose between 'single', 'double', or 'longdouble'.
        Default is 'double', in which case the output array will be composed of
        128-bit complex floats.

    Returns
    -------
    out : ndarray of complex floats
    """
    from numpy.random import ranf
    return ranf(shape).astype(ftype) + 1j * ranf(shape).astype(ftype)


def rand_unit_shifted(shape, ftype='double'):
    """Return random values in the [-0.5, 0.5) interval.

    Parameters
    ----------
    shape : int or sequence of ints
        Output shape. For instance, if the shape is ``(m, n)``, then ``m * n``
        samples are drawn.
    ftype : str or dtype, optional
        Output float type. Choose between 'single', 'double', or 'longdouble'.
        Default is 'double', in which case the output array will be composed of
        64-bit floats.

    Returns
    -------
    out: ndarray of floats
    """
    from numpy.random import ranf
    return ranf(shape).astype(ftype) - 0.5
