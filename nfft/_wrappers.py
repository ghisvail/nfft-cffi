# Copyright (c) 2016, Imperial College London
# Copyright (c) 2016, Ghislain Antony Vaillant
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the BSD license. See the accompanying LICENSE file
# or read the terms at https://opensource.org/licenses/BSD-3-Clause.

from __future__ import absolute_import

from ._bindings import ffi, lib
from functools import reduce

__all__ = ("nfft_create_plan", "nfft_destroy_plan", "nfft_precompute_plan",
           "nfft_execute_forward", "nfft_execute_adjoint")


PRE_PHI_HUT = lib.PRE_PHI_HUT
PRE_PSI = lib.PRE_PSI
PRE_FULL_PSI = lib.PRE_FULL_PSI


def nfft_create_plan(N, M, n, m, flags):
    handle = ffi.new("nfft_plan *")
    flags += (lib.FFTW_INIT, lib.FFT_OUT_OF_PLACE, lib.NFFT_SORT_NODES,
              lib.NFFT_OMP_BLOCKWISE_ADJOINT)
    fftw_flags = (lib.FFTW_MEASURE, lib.FFTW_DESTROY_INPUT)
    lib.nfft_init_guru(handle,
                       len(N),
                       ffi.new("const int []", N),
                       M,
                       ffi.new("const int []", n),
                       m,
                       reduce(lambda x, y: x | y, flags, 0),
                       reduce(lambda x, y: x | y, fftw_flags, 0))
    return handle


def nfft_destroy_plan(handle):
    lib.nfft_finalize(handle)


def nfft_precompute_plan(handle, knots_array):
    handle.x = ffi.cast("double *", knots_array.ctypes.data)
    lib.nfft_precompute_one_psi(handle)


def nfft_execute_forward(handle, input_array, output_array):
    handle.f_hat = ffi.cast("fftw_complex *", input_array.ctypes.data)
    handle.f = ffi.cast("fftw_complex *", output_array.ctypes.data)
    lib.nfft_trafo(handle)


def nfft_execute_forward_direct(handle, input_array, output_array):
    handle.f_hat = ffi.cast("fftw_complex *", input_array.ctypes.data)
    handle.f = ffi.cast("fftw_complex *", output_array.ctypes.data)
    lib.nfft_trafo_direct(handle)


def nfft_execute_adjoint(handle, input_array, output_array):
    handle.f = ffi.cast("fftw_complex *", input_array.ctypes.data)
    handle.f_hat = ffi.cast("fftw_complex *", output_array.ctypes.data)  
    lib.nfft_adjoint(handle)


def nfft_execute_adjoint_direct(handle, input_array, output_array):
    handle.f = ffi.cast("fftw_complex *", input_array.ctypes.data)
    handle.f_hat = ffi.cast("fftw_complex *", output_array.ctypes.data)
    lib.nfft_adjoint_direct(handle)
