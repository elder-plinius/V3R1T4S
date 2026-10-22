#include <stdio.h>
#include <stdlib.h>

typedef long mpfr_prec_t;
typedef int mpfr_sign_t;
typedef long mpfr_exp_t;
typedef unsigned long mp_limb_t;
typedef struct {
    mpfr_prec_t _mpfr_prec;
    mpfr_sign_t _mpfr_sign;
    mpfr_exp_t _mpfr_exp;
    mp_limb_t *_mpfr_d;
} __mpfr_struct;
typedef __mpfr_struct mpfr_t[1];
typedef __mpfr_struct *mpfr_ptr;
typedef const __mpfr_struct *mpfr_srcptr;
typedef int mpfr_rnd_t;
#define MPFR_RNDN 0

void mpfr_init2(mpfr_ptr, mpfr_prec_t);
void mpfr_clear(mpfr_ptr);
int mpfr_const_pi(mpfr_ptr, mpfr_rnd_t);
int mpfr_printf(const char *, ...);

int main() {
    mpfr_t x;
    mpfr_init2(x, 200);
    mpfr_const_pi(x, MPFR_RNDN);
    mpfr_printf("pi = %.50Rf\n", x);
    mpfr_clear(x);
    return 0;
}
