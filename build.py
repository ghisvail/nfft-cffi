# Copyright (c) 2016-2017, Imperial College London
# Copyright (c) 2016-2017, Ghislain Antony Vaillant
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the BSD license. See the accompanying LICENSE file
# or read the terms at https://opensource.org/licenses/BSD-3-Clause.

from cffi import FFI
from pkgconfig import parse


config = parse('nfft3')

cdef = """
typedef ... fftw_complex;

typedef struct {
    fftw_complex *f_hat;
    fftw_complex *f;
    double *x;
    ...;
} nfft_plan;

void nfft_trafo(nfft_plan *);
void nfft_adjoint(nfft_plan *);
void nfft_init_guru(nfft_plan *, int, int *, int, int *, int, unsigned int,
                    unsigned int);
void nfft_precompute_one_psi(nfft_plan *);
void nfft_finalize(nfft_plan *);
"""

source = """
#include <nfft3.h>
"""

ffibuilder = FFI()
ffibuilder.cdef(cdef)
ffibuilder.set_source('nfft._nfft3', source, **config)


if __name__ == '__main__':
    ffibuilder.compile(verbose=True)
