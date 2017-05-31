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
ffibuilder.set_source('_ffi', source, **config)


if __name__ == '__main__':
    ffibuilder.compile(verbose=True)
