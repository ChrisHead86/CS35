#include <cpuid.h>
#include <immintrin.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "./extra.h"

long int x, y;
struct drand48_data buffer = {0};

void
mrand48r_init (void)
{
  srand48_r(time(NULL), &buffer);
}

unsigned long long
mrand48r (void)
{
  mrand48_r(&buffer, &x);
  mrand48_r(&buffer, &y);
  unsigned long long int ret = (((unsigned long long) x) << 32) | ((unsigned  long
								    long) y & 0x00000000FFFFFFFF);
  return ret;
}

void
mrand48r_fini (void)
{
}
