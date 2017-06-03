"""Common utility functions."""
from numpy.random import ranf

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
    return ranf(shape).astype(ftype) - 0.5
