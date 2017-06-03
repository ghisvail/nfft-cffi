# Copyright (c) 2016-2017, Imperial College London
# Copyright (c) 2016-2017, Ghislain Antony Vaillant
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the BSD license. See the accompanying LICENSE file
# or read the terms at https://opensource.org/licenses/BSD-3-Clause.

def dft(f_hat, x):
    from numpy import mgrid, exp, dot, pi
    d = f_hat.ndim
    N = f_hat.shape
    k = mgrid[[slice(-Nt/2, Nt/2) for Nt in N]]
    k = k.reshape([d, -1])
    x = x.reshape([-1, d])
    F = exp(-2j * pi * dot(x, k))
    f = dot(F, f_hat.ravel())
    return f


def dfth(f, x, N):
    from numpy import mgrid, exp, dot, pi, conjugate
    d = len(N)
    k = mgrid[[slice(-Nt/2, Nt/2) for Nt in N]]
    k = k.reshape([d, -1])
    x = x.reshape([-1, d])
    F = exp(-2j * pi * dot(x, k))
    f_hat_dft = dot(conjugate(F).T, f)
    f_hat = f_hat_dft.reshape(N)
    return f_hat


def check_forward(f_hat, f, x):
    from numpy.testing import assert_allclose
    from nfft.nfft import nfft
    assert_allclose(nfft(f_hat, x), dft(f_hat, x))


def check_adjoint(f_hat, f, x):
    from numpy.testing import assert_allclose
    from nfft.nfft import nffth
    assert_allclose(nffth(f, x, f_hat.shape), dfth(f, x, f_hat.shape))


tested_args = (
    ((64,), 64),
    ((256,), 256),
    ((1024,), 1024),
    ((32, 32), 32*32),
    ((64, 64), 64*64),
    ((96, 96), 96*96),
)


def test_all():
    from nfft.util import rand_unit_complex, rand_unit_shifted
    for N, M in tested_args:
        f_hat = rand_unit_complex(N)
        f = rand_unit_complex(M)
        x = rand_unit_shifted([f.size, f_hat.ndim])
        # FIXME: Use of yield to generate test cases is deprecated.
        yield check_forward, f_hat, f, x
        yield check_adjoint, f_hat, f, x
