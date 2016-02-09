# Copyright (c) 2016, Imperial College London
# Copyright (c) 2016, Ghislain Antony Vaillant
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the BSD license. See the accompanying LICENSE file
# or read the terms at https://opensource.org/licenses/BSD-3-Clause.

from __future__ import absolute_import, division
from nfft.nfft import Plan
import numpy
import numpy.random as random
import numpy.testing as testing
from numpy import pi


def ranf_unit_complex(shape, dtype=None):
    def fillvalue(*args, **kwargs):
        return random.ranf() + 1j * random.ranf()
    return numpy.fromfunction(
        function=fillvalue, shape=shape, dtype=dtype)


def ranf_unit_shifted(shape, dtype=None):
    def fillvalue(*args, **kwargs):
        return random.ranf() - 0.5
    return numpy.fromfunction(
        function=fillvalue, shape=shape, dtype=dtype)


def forward_dft(f_hat, x):
    d = f_hat.ndim
    N = f_hat.shape
    k = numpy.mgrid[[slice(-Nt/2, Nt/2) for Nt in N]]
    k = k.reshape([d, -1])
    x = x.reshape([-1, d])
    F = numpy.exp(-2j * pi * numpy.dot(x, k))
    f = numpy.dot(F, f_hat.ravel())
    return f


def adjoint_dft(f, x, N):
    d = len(N)
    k = numpy.mgrid[[slice(-Nt/2, Nt/2) for Nt in N]]
    k = k.reshape([d, -1])
    x = x.reshape([-1, d])
    F = numpy.exp(-2j * pi * numpy.dot(x, k))
    f_hat_dft = numpy.dot(numpy.conjugate(F).T, f)
    f_hat = f_hat_dft.reshape(N)        
    return f_hat


def check_forward(plan):
    testing.assert_allclose(plan.forward(),
                            forward_dft(plan.f_hat, plan.x))


def check_forward_direct(plan):
    testing.assert_allclose(plan.forward(direct=True),
                            forward_dft(plan.f_hat, plan.x))


def check_adjoint(plan):
    testing.assert_allclose(plan.adjoint(),
                            adjoint_dft(plan.f, plan.x, plan.f_hat.shape))


def check_adjoint_direct(plan):
    testing.assert_allclose(plan.adjoint(direct=True),
                            adjoint_dft(plan.f, plan.x, plan.f_hat.shape))


tested_args = (
    dict(N=(64,), M=64),
    dict(N=(256,), M=256),
    dict(N=(1024,), M=1024),
    dict(N=(32, 32), M=32*32),
    dict(N=(64, 64), M=64*64),
    dict(N=(96, 96), M=96*96),
)


def test_forward():
    for args in tested_args:
        plan = Plan(**args)
        numpy.copyto(plan.x,
                     ranf_unit_shifted(plan.x.shape, plan.x.dtype))
        numpy.copyto(plan.f_hat,
                     ranf_unit_complex(plan.f_hat.shape, plan.f_hat.dtype))
        plan.precompute()
        yield check_forward, plan


def test_forward_direct():
    for args in tested_args:
        plan = Plan(**args)
        numpy.copyto(plan.x,
                     ranf_unit_shifted(plan.x.shape, plan.x.dtype))
        numpy.copyto(plan.f_hat,
                     ranf_unit_complex(plan.f_hat.shape, plan.f_hat.dtype))
        plan.precompute()
        yield check_forward_direct, plan


def test_adjoint():
    for args in tested_args:
        plan = Plan(**args)
        numpy.copyto(plan.x,
                     ranf_unit_shifted(plan.x.shape, plan.x.dtype))
        numpy.copyto(plan.f_hat,
                     ranf_unit_complex(plan.f.shape, plan.f.dtype))
        plan.precompute()
        yield check_adjoint, plan


def test_adjoint_direct():
    for args in tested_args:
        plan = Plan(**args)
        numpy.copyto(plan.x,
                     ranf_unit_shifted(plan.x.shape, plan.x.dtype))
        numpy.copyto(plan.f,
                     ranf_unit_complex(plan.f.shape, plan.f.dtype))
        plan.precompute()
        yield check_adjoint_direct, plan
