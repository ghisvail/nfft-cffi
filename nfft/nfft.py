# Copyright (c) 2016, Imperial College London
# Copyright (c) 2016, Ghislain Antony Vaillant
# All rights reserved.
#
# Distributed under the terms of the new BSD license.
# See the accompanying LICENSE file or read the terms at
# https://opensource.org/licenses/BSD-3-Clause.

from ._nfft import ffi, lib
from functools import reduce
import numpy

__all__ = ("Plan")


class Plan(object):
  
    """The NFFT plan class."""
    
    def __init__(self, N, M, *args, **kwargs):
        "Instantiate the NFFT plan."        
        d = len(N)
        n = [2 * Nt for Nt in N]
        # TODO: auto-adjust with desired dtype.
        m = 6
        # TODO: auto-adjust with desired precomputation.
        nfft_flags = (lib.PRE_PHI_HUT, lib.PRE_PSI, lib.FFT_OUT_OF_PLACE,
                      lib.FFTW_INIT)
        fftw_flags = (lib.FFTW_ESTIMATE, lib.FFTW_DESTROY_INPUT)
        # Create plan handle.
        handle = ffi.new("nfft_plan *")
        lib.nfft_init_guru(handle, d, ffi.new("const int []", N), M,
            ffi.new("const int []", n), m,
            reduce(lambda x, y: x | y, nfft_flags, 0),
            reduce(lambda x, y: x | y, fftw_flags, 0))
        # Create and bind f_hat array.
        f_hat = numpy.empty(N, dtype=numpy.complex128)
        handle.f_hat = ffi.cast("fftw_complex *", f_hat.ctypes.data)
        # Create and bind f array.
        f = numpy.empty(M, dtype=numpy.complex128)
        handle.f = ffi.cast("fftw_complex *", f.ctypes.data)
        # Create and bind x array.
        if d == 1:
            x = numpy.empty(M, dtype=numpy.float64)
        else:
            x = numpy.empty([M, d], dtype=numpy.float64)
        handle.x = ffi.cast("double *", x.ctypes.data)
        # Hold plan handle and interface arrays together.
        self.__handle = handle
        self.f_hat = f_hat
        self.f = f
        self.x = x
        # TODO: support precompute on instantiation.

    def __del__(self):
        lib.nfft_finalize(self.__handle)

    def forward(self, direct=False):
        """Compute and return the forward transform."""
        if direct:
            self.execute_forward_direct()
        else:
            self.execute_forward()
        return self.f

    def execute_forward(self):
        """Perform the foward transform (fast)."""
        lib.nfft_trafo(self.__handle)

    def execute_forward_direct(self):
        """Perform the forward transform (direct)."""
        lib.nfft_trafo_direct(self.__handle)

    def adjoint(self, direct=False):
        """Compute and return the adjoint transform."""
        if direct:
            self.execute_adjoint_direct()
        else:
            self.execute_adjoint()
        return self.f_hat

    def execute_adjoint(self):
        """Perform the adjoint transform (fast)."""
        lib.nfft_adjoint(self.__handle)

    def execute_adjoint_direct(self):
        """Compute the adjoint transform (direct)."""
        lib.nfft_adjoint_direct(self.__handle)

    def precompute(self):
        "Precompute the plan."
        lib.nfft_precompute_one_psi(self.__handle)