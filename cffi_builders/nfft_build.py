# Copyright (c) 2016, Imperial College London
# Copyright (c) 2016, Ghislain Antony Vaillant
# All rights reserved.
#
# Distributed under the terms of the new BSD license.
# See the accompanying LICENSE file or read the terms at
# https://opensource.org/licenses/BSD-3-Clause.

from cffi import FFI
import pkgconfig


if not pkgconfig.exists("nfft3"):
    raise RuntimeError("NFFT library not found via pkgconfig.")
pc_nfft3 = {key: list(val) for (key, val) in pkgconfig.parse("nfft3").items()}

ffi = FFI()

ffi.cdef("""
    typedef ... fftw_complex;
    
    #define FFTW_ESTIMATE ...
    #define FFTW_DESTROY_INPUT ...    
    
    typedef struct {
        fftw_complex *f_hat;
        fftw_complex *f;
        double *x;
        ...; 
    } nfft_plan;

    void nfft_trafo_direct(nfft_plan *);
    void nfft_adjoint_direct(nfft_plan *);     
    void nfft_trafo(nfft_plan *);
    void nfft_adjoint(nfft_plan *);    
    void nfft_init_guru(nfft_plan *, int, int *, int, int *, int, unsigned int,
                        unsigned int);    
    void nfft_precompute_one_psi(nfft_plan *); 
    void nfft_finalize(nfft_plan *);
        
    #define PRE_PHI_HUT ...
    #define FG_PSI ...
    #define PRE_LIN_PSI ...
    #define PRE_FG_PSI ...
    #define PRE_PSI ...
    #define PRE_FULL_PSI ...
    #define MALLOC_X ...
    #define MALLOC_F_HAT ...
    #define MALLOC_F ...
    #define FFT_OUT_OF_PLACE ...
    #define FFTW_INIT ...
    #define NFFT_SORT_NODES ...
    #define NFFT_OMP_BLOCKWISE_ADJOINT ...
    #define PRE_ONE_PSI ...
    """
)

ffi.set_source(
    "_nfft",
    """    
    #include <nfft3.h>
    """,
    **pc_nfft3
)