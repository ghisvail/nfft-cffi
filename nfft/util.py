from numpy.random import ranf

__all__ = ('rand_unit_complex', 'rand_unit_shifted')


def rand_unit_complex(shape, ftype='double'):
    return ranf(shape).astype(ftype) + 1j * ranf(shape).astype(ftype)


def rand_unit_shifted(shape, ftype='double'):
    return ranf(shape).astype(ftype) - 0.5
